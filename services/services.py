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
import waitress
import connexion
from threading import Thread
import importlib.resources as resources

from dtaservice.dtaservice_pb2_grpc import DTAServerStub

import doctrans_py_swagger_server
from doctrans_py_swagger_server import encoder

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
        log.warning("no app name was specified instead using: UNKNOWN!")
        dts = pb.DocTransServer(
            AppName=app_name,
            CfgFile=str(
                working_home_dir / Path("/.dta/") / app_name / Path("/config.json")
            ),
            LogLevel="INFO",
        )

        # parse arguments to populate the configuration
        args = parser.parse_args()
        for arg in vars(args).items():
            if arg[1]:
                setattr(dts, arg[0], arg[1])

        log.getLogger().setLevel(log._nameToLevel[dts.LogLevel])

        if dts.Init:
            dts.new_config_file()

        # grpc is necessary for internal communication. REST is optional.
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

        swagger_server_module_path = Path(doctrans_py_swagger_server.__file__).parent
        swagger_path = swagger_server_module_path / Path("swagger")

        app = connexion.App(__name__, specification_dir=swagger_path)
        app.app.json_ecoder = encoder.JSONEncoder
        app.add_api(
            "swagger.yaml",
            arguments={"title": "dtaservice.proto"},
            pythonic_params=True,
        )
        rest_thread = Thread(target=waitress.serve, args=(app,), daemon=True)
        rest_thread.start()

        # print(vars(doctrans_py_swagger_server))

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

        server.wait_for_termination()
