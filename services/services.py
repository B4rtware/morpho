from abc import ABC, abstractmethod
from pathlib import Path
import sys
from typing import Optional, Tuple
import grpc
import concurrent.futures as futures
import argparse

sys.path.append(str(Path(".").resolve()))

import dtaservice.doctransserver as pb
import dtaservice.dtaservice_pb2_grpc as dtaservice_pb2_grpc
import dtaservice.dtaservice_pb2 as dtaservice_pb2

parser = argparse.ArgumentParser()
parser.add_argument_group("Registrar")
parser.add_argument("--RegistrarURL", type=str, help="Registry URL")
parser.add_argument(
    "--RegistrarUser", type=str, help="Registry User, no user used if not provided"
)
# parser.add_argument("--RegistrarPwd-pwd",  type=str, help="Registry User Password, no password used if not provided")
parser.add_argument(
    "--TTL", type=int, help="Time in seconds to reregister at Registrar."
)
parser.add_argument_group("Service")
parser.add_argument(
    "--HostName",
    type=str,
    help="If provided will be used as hostname, else automatically derived.",
)
parser.add_argument(
    "--AppName", type=str, help="ID of the service as e.g. 'DOC.TXT.COUNT.'"
)
parser.add_argument(
    "--PortToListen", type=str, help="On which port to listen for this service."
)
parser.add_argument(
    "--DtaType",
    type=str,
    help="One of Gateway or Service. Service is assumed if not provided.",
)
parser.add_argument("--IsSSL", type=str, help="Can the service be reached via SSL.")
parser.add_argument_group("Generic")
parser.add_argument(
    "--LogLevel",
    type=int,
    help="Log level, one of panic, fatal, error, warn or warning, info, debug, trace",
)
parser.add_argument("--CfgFile", type=str, help="The config file to use")
parser.add_argument(
    "--Init",
    help="Create a default config file as defined by cfg-file, if set. If not set ~/.dta/<AppName>/config.json will be created.",
    action="store_true",
)
parser.add_argument(
    "--Trace",
    help="Create Proxy for capturing traces from and to this microservice",
    action="store_true",
)

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
    def run(cls, port):
        working_home_dir = Path.home()

        dts = pb.DocTransServer(
            RegistrarURL="http://127.0.0.1:8761/eureka", PortToListen=port
        )

        # parse to fill the configuration
        args = parser.parse_args()
        for arg in vars(args).items():
            if arg[1]:
                setattr(dts, arg[0], arg[1])

        if dts.Init:
            dts.new_config_file()

        # max_port_seeks = 20
        # # dts.create_listener(max_port_seeks)

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        server.add_insecure_port(f"[::]:{port}")
        # #s.start()

        dtaservice_pb2_grpc.add_DTAServerServicer_to_server(cls(), server)
        server.start()

        server.wait_for_termination()
