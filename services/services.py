from abc import ABC, abstractmethod
from dataclasses import dataclass
import dataclasses
from pathlib import Path
import sys
from typing import Optional, Tuple
import grpc
import concurrent.futures as futures
import argparse
import py_eureka_client.eureka_client as eureka_client
from dtaservice.dtaservice_pb2 import DocumentRequest
import colorama as cr
import urllib


from dtaservice.dtaservice_pb2_grpc import DTAServerStub

sys.path.append(str(Path(".").resolve()))
from dtslog import log
import dtaservice.doctransserver as pb
import dtaservice.dtaservice_pb2_grpc as dtaservice_pb2_grpc
import dtaservice.dtaservice_pb2 as dtaservice_pb2

cr.init()

parser = argparse.ArgumentParser()
# fmt: off
parser.add_argument_group("Registrar")
parser.add_argument("--Register", action="store_true", help="Register service with EUREKA, if set")
parser.add_argument("--RegistrarURL", type=str, help="Registry URL")
parser.add_argument("--RegistrarUser", type=str, help="Registry User, no user used if not provided")
parser.add_argument("--RegistrarPwd",  type=str, help="Registry User Password, no password used if not provided")
parser.add_argument("--TTL", type=int, help="Time in seconds to reregister at Registrar.")

parser.add_argument_group("Service")
parser.add_argument("--HostName", type=str, help="If provided will be used as hostname, else automatically derived.")
parser.add_argument("--AppName", type=str, help="ID of the service as e.g. 'DOC.TXT.COUNT.'")
parser.add_argument("--PortToListen", type=str, help="On which port to listen for this service.")
parser.add_argument("--DtaType", type=str, help="One of Gateway or Service. Service is assumed if not provided.")
parser.add_argument("--IsSSL", type=str, help="Can the service be reached via SSL.")
parser.add_argument("--REST", action="store_true", help="REST-API enabled on port 80, if set.")
parser.add_argument("--HTTPPort", type=str, help="On which httpPort to listen for REST, if enableREST is set. Ignored otherwise.")

parser.add_argument_group("Generic")
parser.add_argument("--LogLevel", type=str, help="Log level, one of panic, fatal, error, warn or warning, info, debug, trace", default="INFO", choices=("CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"))
parser.add_argument("--CfgFile", type=str, help="The config file to use")
parser.add_argument("--Init", help="Create a default config file as defined by cfg-file, if set. If not set ~/.dta/<AppName>/config.json will be created.", action="store_true")
parser.add_argument("--Trace", help="Connect Proxy for capturing traces to this microservice", action="store_true")
# fmt: on


@dataclass
class DtaService:
    service_handler: pb.DocTransServer
    resolver: eureka_client.RegistryClient


QDS_PROXY_APP_NAME = "DE.TU-Berlin.QDS.PROXY"


class DTAServer(ABC, dtaservice_pb2_grpc.DTAServerServicer):
    @abstractmethod
    def work(self, request, context) -> Tuple[str, Optional[str]]:
        pass

    def TransformDocument(self, request, context):
        document, error = self.work(request, context)
        return dtaservice_pb2.TransformDocumentResponse(
            # TODO: error needs to be implemented
            trans_document=document.encode(),
            trans_output=document,
            error=error,
        )

    def ListServices(self, request: dtaservice_pb2.ListServiceRequest, context):
        services = []
        return dtaservice_pb2.ListServicesResponse(services=services)

    @classmethod
    def run(cls):
        working_home_dir = Path.home()

        app_name = getattr(cls, "app_name", "UNKNOWN")
        dts = pb.DocTransServer(
            AppName=app_name,
            CfgFile=str(
                working_home_dir / Path("/.dta/") / app_name / Path("/config.json")
            ),
            LogLevel="INFO",
        )

        # parse to fill the configuration
        args = parser.parse_args()
        for arg in vars(args).items():
            if arg[1]:
                setattr(dts, arg[0], arg[1])

        log.getLogger().setLevel(log._nameToLevel[dts.LogLevel])

        if dts.Init:
            dts.new_config_file()

        # register at eureka server
        eureka_client.init_registry_client(
            eureka_server=dts.RegistrarURL,
            instance_id=dts.HostName,
            app_name=dts.AppName,
            instance_port=int(dts.PortToListen),
            instance_secure_port_enabled=dts.IsSSL,
            metadata={"DTA-Type": dts.DtaType},
        )

        # create grpc server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        # TODO: there is currently no case if the port is already in use
        server.add_insecure_port(f"[::]:{dts.PortToListen}")

        cls_instance = cls()
        # bind properties to be used inside the class instance
        cls.dts = dts
        dtaservice_pb2_grpc.add_DTAServerServicer_to_server(cls_instance, server)
        server.start()

        # fmt: off
        if __debug__:
            # use -O flag to remove all debug branches out of the bytecode
            print("")
            print(" +-------" + "-" * len(app_name) + "-------+")
            print(f" |       {cr.Back.GREEN + cr.Fore.BLACK + app_name + cr.Back.RESET + cr.Fore.RESET}       |")
            print(" +-------" + "-" * len(app_name) + "-------+")
            for setting in dataclasses.asdict(dts).items():
                print(f" |- {setting[0]:<15} - {setting[1]}")
            print("")
            print(f" -> listening on port {dts.PortToListen}")
            print("")
            print(cr.Fore.YELLOW + "     You see this message because __debug__ is true.")
            print("     Use the -O flag to enable optimization `python -O`." + cr.Fore.RESET)
            print("")
        # fmt: on
        
        if dts.Trace:
            # FIXME: if the client disconnects it the proxy still sends heart beats
            # Maybe this can be fixed the proxy is looking for the client if it
            # does not find the application it should delete it.
            # But then the application proxy is till in the record ...
            # get proxy instance if its avialable
            proxy_service = None
            try:
                proxy_service = eureka_client.get_application(
                    dts.RegistrarURL, QDS_PROXY_APP_NAME
                )
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    log.error("no proxy for capturing traces was found")
                    exit(1)

            instance = proxy_service.instances[0]
            # TODO: the docuement request is just a work around events or something similar should be used
            # send register notification
            with grpc.insecure_channel(
                f"{instance.ipAddr}:{instance.port.port}"
            ) as channel:
                stub = DTAServerStub(channel)
                result = stub.TransformDocument(
                    DocumentRequest(
                        service_name=app_name,
                        document="REGISTER ME - id:59e46078-6ca5-4f0b-9732-e6fdf5f5a49e".encode(),
                    )
                )
                if (
                    result.trans_document.decode()
                    == "OK - id:59e46078-6ca5-4f0b-9732-e6fdf5f5a49e"
                ):
                    log.info(f"successfully send proxy registration")

        server.wait_for_termination()
