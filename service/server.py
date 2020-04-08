from abc import ABC, abstractmethod
from dataclasses import dataclass
import dataclasses
from pathlib import Path
import sys
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    TypedDict,
    NewType,
)
import grpc
import concurrent.futures as futures
import argparse
from grpc import ServicerContext
import py_eureka_client.eureka_client as eureka_client
import colorama as cr
import waitress
import connexion
from threading import Thread
from connexion import RestyResolver
from flask import Flask
from contextlib import redirect_stdout, redirect_stderr
import io
import traceback

import doctrans_py_swagger_server
from doctrans_py_swagger_server.models import DtaserviceTransformDocumentResponse


sys.path.append(str(Path(".").resolve()))
from service.log import log
from service.config import DTAServerConfig

from service.proto.dtaservice_pb2_grpc import add_DTAServerServicer_to_server
from service.proto.dtaservice_pb2 import DocumentRequest, TransformDocumentResponse
from service.proto.dtaservice_pb2 import ListServicesResponse
from service.proto.dtaservice_pb2 import ListServiceRequest
from service.proto.dtaservice_pb2_grpc import DTAServerServicer
from service.rest import Status


cr.init()


class RawTransformDocumentResponse(TypedDict):
    trans_document: Optional[str]
    trans_output: List[str]
    error: List[str]


Options = NewType("Options", Dict[str, str])


# class Status(Enum)


# TODO: verify that all options are used or at least output a warning
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
parser.add_argument("--Protocols", type=str, nargs='+', help="Which protocoly should be used by the server.", default=["rest"], choices=("rest", "grpc"))

parser.add_argument_group("Generic")
parser.add_argument("--LogLevel", type=str, help="Log level, one of panic, fatal, error, warn or warning, info, debug, trace", default="INFO", choices=("CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"))
parser.add_argument("--CfgFile", type=str, help="The config file to use")
parser.add_argument("--Init", help="Create a default config file as defined by cfg-file, if set. If not set ~/.dta/<AppName>/config.json will be created.", action="store_true")
# fmt: on

# TODO: consider remove this
@dataclass
class DtaService:
    service_handler: DTAServerConfig
    resolver: eureka_client.RegistryClient


QDS_PROXY_APP_NAME = "DE.TU-Berlin.QDS.PROXY"







# class DTARestServer(object):
#     def __init__(self, worker: Callable[[str], str], config: DTAServerConfig):
#         self._work = worker
#         self.config = config
#         self.app = Flask(__name__)
#         # TODO: try to use decorator
#         # fmt: off
#         self.app.add_url_rule("/v1/qds/dta/document/transform", "transform", self.transform)
#         self.app.add_url_rule("/v1/qds/dta/service/list", "list", self.list)
#         self.app.add_url_rule("/v1/qds/dta/document/transform-pipe", "pipe", self.transform_pipe)
#         # fmt: on

#         # as deamon so that the thread gets also terminated if the parent
#         # self.rest_thread = Thread(
#         #     target=waitress.serve,
#         #     args=(self.app,),
#         #     kwargs={"port": int(config.HTTPPort), "_quiet": True},
#         #     daemon=True,
#         # )

#     def transform(self) -> Tuple[RawTransformDocumentResponse, Status, Dict[str, str]]:
#         trans_document = None
#         captured_stdout = io.StringIO()
#         captured_stderr = io.StringIO()
#         with redirect_stderr(captured_stderr):
#             with redirect_stdout(captured_stdout):
#                 try:
#                     trans_document = self._work("work")
#                 except BaseException:
#                     traceback.print_exc()
#         error = captured_stderr.getvalue().split("\n")
#         trans_output = captured_stdout.getvalue().split("\n")

#         return (
#             {
#                 "trans_document": trans_document,
#                 "trans_output": trans_output,
#                 "error": error,
#             },
#             Status.OK if not error else Status.INTERNAL_SERVER_ERROR,
#             {"Content-Type": "application/json"},
#         )

#     def list(self, request, response):
#         pass

#     def transform_pipe(self, request, response):
#         pass

#     def create_rest_thread(self):
#         return Thread(
#             target=waitress.serve,
#             args=(self.app,),
#             kwargs={"port": int(self.config.HTTPPort), "_quiet": True},
#             daemon=True,
#         )


# class DTAGrpcServer(object):
#     pass


# class DTAServer(ABC, DTAServerServicer, DTARestServer):
#     def __init__(self, config: DTAServerConfig) -> None:
#         print("init dtaserver")
#         self.config = config
#         super().__init__(self.rest_work, self.config)
#         self.rest_thread = self.create_rest_thread()

#     @abstractmethod
#     def work(
#         self, request: DocumentRequest, context: ServicerContext
#     ) -> Tuple[str, Optional[str]]:
#         pass

#     @abstractmethod
#     def rest_work(self, document: str) -> str:
#         pass

#     #
#     # GRPC functions
#     #

#     def TransformDocument(
#         self, request: DocumentRequest, context: ServicerContext
#     ) -> TransformDocumentResponse:
#         document, error = self.work(request, context)
#         return TransformDocumentResponse(
#             # TODO: error needs to be implemented
#             trans_document=document.encode(),
#             trans_output=document,
#             error=error,
#         )

#     def ListServices(
#         self, request: ListServiceRequest, context: ServicerContext
#     ) -> ListServicesResponse:
#         services = []
#         return ListServicesResponse(services=services)

#     #
#     # Rest functions
#     #

#     # def rest_transform_document(self, body: str) -> Tuple[Dict[str, str], int]:
#     #     document, error = self.work()
#     #     return DtaserviceTransformDocumentResponse(
#     #         trans_document=
#     #     ), 200

#     # def rest_list(self):
#     #     pass

#     @classmethod
#     def run(cls):
#         print("execute run")
#         working_home_dir = Path.home()

#         # TODO: rename app_name to name
#         app_name = getattr(cls, "app_name", "UNKNOWN")
#         if app_name == "UNKNOWN":
#             log.warning("no app name was specified instead using: UNKNOWN!")
#         # doctrans: dts
#         config = DTAServerConfig(
#             AppName=app_name,
#             CfgFile=str(
#                 working_home_dir / Path("/.dta/") / app_name / Path("/config.json")
#             ),
#             LogLevel="INFO",
#         )

#         # parse arguments to populate the configuration
#         args = parser.parse_args()
#         for arg in vars(args).items():
#             if arg[1]:
#                 setattr(config, arg[0], arg[1])

#         log.getLogger().setLevel(config.LogLevel)

#         # create new config file by saving the default values
#         if config.Init:
#             config.save()
#             log.info(
#                 "Wrote example configuration file to {}. Exiting".format(config.CfgFile)
#             )
#             exit(0)
#             return

#         # grpc is necessary for internal communication. REST is optional.
#         # register at eureka server
#         if config.Register:
#             eureka_client.init_registry_client(
#                 eureka_server=config.RegistrarURL,
#                 instance_id=config.HostName,
#                 app_name=config.AppName,
#                 instance_port=int(config.PortToListen),
#                 instance_secure_port_enabled=config.IsSSL,
#                 # TODO: change dta type name to use the same from the rest specification
#                 metadata={"DTA-Type": config.DtaType},
#             )

#         # TODO: add flag to not use grpc
#         # create grpc server
#         server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#         # TODO: there is currently no case if the port is already in use
#         server.add_insecure_port(f"[::]:{config.PortToListen}")

#         cls_instance = cls(config)
#         # bind properties to be used inside the class instance
#         add_DTAServerServicer_to_server(cls_instance, server)
#         server.start()

#         if config.REST:
#             cls_instance.rest_thread.start()
#             # TODO: check if rest_thread needs to added to the cls instance
#             # swagger_server_module_path = Path(
#             #     doctrans_py_swagger_server.__file__
#             # ).parent
#             # swagger_path = swagger_server_module_path / Path("swagger")

#             # app = connexion.App(__name__, specification_dir=swagger_path)
#             # app.app.json_ecoder = encoder.JSONEncoder
#             # app.add_api(
#             #     "swagger.yaml",
#             #     arguments={"title": "dtaservice.proto"},
#             #     options={"controllers": "service.rest.controller"},
#             #     pythonic_params=True,
#             #     resolver=RestyResolver("service.rest.controller"),
#             # )

#             # TODO: check rest function are present

#             # app = Flask(__name__)
#             # app.add_url_rule(
#             #     "/v1/dta/service/list",
#             #     "list",
#             #     cls_instance.rest_transform_document,
#             #     methods=["GET"],
#             # )
#             # app.add_url_rule(
#             #     "/v1/dta/document/transform",
#             #     "transform",
#             #     cls_instance.rest_transform_document,
#             #     methods=["POST"],
#             # )

#             # as deamon so that the thread gets also terminated if the parent
#             # rest_thread = Thread(
#             #     target=waitress.serve,
#             #     args=(app,),
#             #     kwargs={"port": int(config.HTTPPort), "_quiet": True},
#             #     daemon=True,
#             # )
#             # self.create_rest_thread()
#             # rest_thread.start()

#         # fmt: off
#         if __debug__:
#             # use -O flag to remove all debug branches out of the bytecode
#             print("")
#             print(" +-------" + "-" * len(app_name) + "-------+")
#             print(f" |       {cr.Back.GREEN + cr.Fore.BLACK + app_name + cr.Back.RESET + cr.Fore.RESET}       |")
#             print(" +-------" + "-" * len(app_name) + "-------+")
#             for setting in dataclasses.asdict(config).items():
#                 print(f" |- {setting[0]:<15} - {setting[1]}")
#             print("")
#             print(f" [grpc] -> listening on port {config.PortToListen}")
#             if config.REST: print(f" [rest] -> listening on port {config.HTTPPort}")
#             print("")
#             print(cr.Fore.YELLOW + "     You see this message because __debug__ is true.")
#             print("     Use the -O flag to enable optimization `python -O`." + cr.Fore.RESET)
#             print("")
#         # fmt: on

#         server.wait_for_termination()

class DTARestWorkConsumer(object):
    def __init__(self, work):
        self._work = work
        self.app = Flask(__name__)
        # TODO: try to use decorator
        # fmt: off
        self.app.add_url_rule("/v1/qds/dta/document/transform", "transform", self._transform)
        self.app.add_url_rule("/v1/qds/dta/service/list", "list", self._list)
        self.app.add_url_rule("/v1/qds/dta/document/transform-pipe", "pipe", self._transform_pipe)
        # fmt: on

    def _transform(self) -> Tuple[RawTransformDocumentResponse, Status, Dict[str, str]]:
        trans_document = None
        captured_stdout = io.StringIO()
        captured_stderr = io.StringIO()
        with redirect_stderr(captured_stderr):
            with redirect_stdout(captured_stdout):
                try:
                    trans_document = self._work("work")
                except BaseException:
                    traceback.print_exc()
        error = captured_stderr.getvalue().split("\n")
        trans_output = captured_stdout.getvalue().split("\n")

        return (
            {
                "trans_document": trans_document,
                "trans_output": trans_output,
                "error": error,
            },
            Status.OK if not error else Status.INTERNAL_SERVER_ERROR,
            {"Content-Type": "application/json"},
        )

    def _list(self, request, response):
        pass

    def _transform_pipe(self, request, response):
        pass

    def start(self):
        thread = Thread(
            daemon=True,
            target=waitress.serve,
            args=(self.app,),
            kwargs={"port": 8080, "_quiet": True},
        )
        thread.start()
        return thread

class DTAGrpcWorkConsumer(DTAServerServicer):
    def __init__(self, work) -> None:
        self._work = work

    def TransformDocument(self, request: DocumentRequest, context: ServicerContext) -> TransformDocumentResponse:
        trans_document = "sdsd" #self._work("LOOOL")
        return TransformDocumentResponse(
            # TODO: error needs to be implemented
            trans_document=trans_document,
            trans_output=document,
            error=error,
        )

    def ListServices(
        self, request: ListServiceRequest, context: ServicerContext
    ) -> ListServicesResponse:
        services = []
        return ListServicesResponse(services=services)

    def start(self):
        print("starting grpc")

protocols = {
    "rest": DTARestWorkConsumer,
    "grpc": DTAGrpcWorkConsumer
}

class DTAServer(ABC):
    def __init__(self) -> None:
        print("init dtaserver")
        # self.config = config

    @abstractmethod
    def work(self, document: str) -> str:
        pass

    @classmethod
    def run(cls):
        print("execute run")
        working_home_dir = Path.home()

        # TODO: rename app_name to name
        app_name = getattr(cls, "app_name", "UNKNOWN")
        if app_name == "UNKNOWN":
            log.warning("no app name was specified instead using: UNKNOWN!")
        # doctrans: dts
        config = DTAServerConfig(
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
                setattr(config, arg[0], arg[1])

        log.getLogger().setLevel(config.LogLevel)

        # create new config file by saving the default values
        if config.Init:
            config.save()
            log.info(
                "Wrote example configuration file to {}. Exiting".format(config.CfgFile)
            )
            exit(0)
            return

        # register at eureka server
        if config.Register:
            eureka_client.init_registry_client(
                eureka_server=config.RegistrarURL,
                instance_id=config.HostName,
                app_name=config.AppName,
                instance_port=int(config.PortToListen),
                instance_secure_port_enabled=config.IsSSL,
                # TODO: change dta type name to use the same from the rest specification
                metadata={"DTA-Type": config.DtaType},
            )

        # TODO: add flag to not use grpc
        # create grpc server
        # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        # TODO: there is currently no case if the port is already in use
        # server.add_insecure_port(f"[::]:{config.PortToListen}")

        cls_instance = cls()
        # bind properties to be used inside the class instance
        #add_DTAServerServicer_to_server(cls_instance, server)
        #server.start()

        # start protocol consumer
        for protocol in args.Protocols:
            instance = protocols[protocol](cls_instance.work)
            instance.start()

        # fmt: off
        if __debug__:
            # use -O flag to remove all debug branches out of the bytecode
            print("")
            print(" +-------" + "-" * len(app_name) + "-------+")
            print(f" |       {cr.Back.GREEN + cr.Fore.BLACK + app_name + cr.Back.RESET + cr.Fore.RESET}       |")
            print(" +-------" + "-" * len(app_name) + "-------+")
            for setting in dataclasses.asdict(config).items():
                print(f" |- {setting[0]:<15} - {setting[1]}")
            print("")
            print(f" [grpc] -> listening on port {config.PortToListen}")
            if config.REST: print(f" [rest] -> listening on port {config.HTTPPort}")
            print("")
            print(cr.Fore.YELLOW + "     You see this message because __debug__ is true.")
            print("     Use the -O flag to enable optimization `python -O`." + cr.Fore.RESET)
            print("")
        # fmt: on

        try:
            input()
        except KeyboardInterrupt:
            pass

        #server.wait_for_termination()

class QDS_TEST(DTAServer):
    def work(self, document: str) -> str:
        return "Work done"


if __name__ == "__main__":

    def work():
        return "work"

    # a = DTARestServer(work)
    # app.run()
    # a = DTARestServerThread(work)
    # thread = a.run()
    # thread.join()
    a = QDS_TEST()
    a.run()

