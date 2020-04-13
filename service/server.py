from abc import ABC, abstractmethod
import argparse
import concurrent.futures as futures
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
import dataclasses
import io
from pathlib import Path
import sys
from threading import Thread
import traceback
from typing import Dict, List, NewType, Optional, Tuple, TypedDict

import colorama as cr
import flask
from flask import Flask

# from flask_swagger_ui import get_swaggerui_blueprint
from swagger_ui import api_doc
import grpc
from grpc import ServicerContext
import waitress
import py_eureka_client.eureka_client as eureka_client

sys.path.append(str(Path(".").resolve()))

from service.config import DTAServerConfig
from service.log import log
from service.proto.dtaservice_pb2 import DocumentRequest, TransformDocumentResponse
from service.proto.dtaservice_pb2 import ListServicesResponse
from service.proto.dtaservice_pb2 import ListServiceRequest
from service.proto.dtaservice_pb2_grpc import add_DTAServerServicer_to_server
from service.proto.dtaservice_pb2_grpc import DTAServerServicer
from service.rest import Status


cr.init()


class RawTransformDocumentResponse(TypedDict):
    trans_document: Optional[str]
    trans_output: List[str]
    error: List[str]


Options = NewType("Options", Dict[str, str])


# TODO: verify that all options are used or at least output a warning
# fmt: off
# pylint: disable=line-too-long
parser = argparse.ArgumentParser() # pylint: disable=invalid-name

parser.add_argument_group("Registrar")
parser.add_argument("--register", action="store_true", help="Register service with EUREKA, if set")
parser.add_argument("--registrar-url", type=str, help="Registry URL")
parser.add_argument("--registrar-user", type=str, help="Registry User, no user used if not provided")
parser.add_argument("--registrar-password", type=str, help="Registry User Password, no password used if not provided")
parser.add_argument("--ttl", type=int, help="Time in seconds to reregister at Registrar.")

parser.add_argument_group("Service")
parser.add_argument("--host-name", type=str, help="If provided will be used as hostname, else automatically derived.")
parser.add_argument("--app-name", type=str, help="ID of the service as e.g. 'DOC.TXT.COUNT.'")
parser.add_argument("--port-to-listen", type=str, help="On which port to listen for this service.")
parser.add_argument("--dta-type", type=str, help="One of Gateway or Service. Service is assumed if not provided.")
parser.add_argument("--is-ssl", type=str, help="Can the service be reached via SSL.")
parser.add_argument("--rest", action="store_true", help="REST-API enabled on port 80, if set.")
parser.add_argument("--http-port", type=str, help="On which httpPort to listen for REST, if enableREST is set. Ignored otherwise.")
parser.add_argument("--protocols", type=str, nargs='+', help="Which protocol should be used by the server.", default=["rest"], choices=("rest", "grpc"))

parser.add_argument_group("Generic")
parser.add_argument("--log-level", type=str, help="Log level, one of panic, fatal, error, warn or warning, info, debug, trace", default="INFO", choices=("CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"))
parser.add_argument("--config-file", type=str, help="The config file to use")
parser.add_argument("--init", help="Create a default config file as defined by cfg-file, if set. If not set ~/.dta/<AppName>/config.json will be created.", action="store_true")
# pylint: enable=line-too-long
# fmt: on


# TODO: consider remove this
@dataclass
class DtaService:
    service_handler: DTAServerConfig
    resolver: eureka_client.RegistryClient


class DTARestWorkConsumer:
    def __init__(self, work, config):
        log.info("initializing DTARestWorkConsumer")
        self._work = work
        self.config = config
        self.app = Flask(__name__)
        # TODO: try to use decorator
        # fmt: off
        # pylint: disable: line-too-long
        working_dir = Path.cwd()
        config_path = working_dir / Path("./service/rest/swagger/openapi.yaml")
        api_doc(self.app, config_path=config_path, url_prefix="/info")
        self.app.add_url_rule("/v1/qds/dta/document/transform", "transform", self.transform_document, methods=["POST"])
        self.app.add_url_rule("/v1/qds/dta/service/list", "list", self.list_services)
        self.app.add_url_rule("/v1/qds/dta/document/transform-pipe", "pipe", self.transform_document_pipe)
        # pylint: enable: line-too-long
        # fmt: on

    # TODO: rename to list services / transform document and transform document pipe
    def transform_document(
        self,
    ) -> Tuple[RawTransformDocumentResponse, Status, Dict[str, str]]:
        trans_document = None
        captured_stdout = io.StringIO()
        captured_stderr = io.StringIO()
        with redirect_stderr(captured_stderr):
            with redirect_stdout(captured_stdout):
                try:
                    trans_document = self._work(flask.request.json.document)
                except BaseException:  # pylint: disable=broad-except
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

    def list_services(self, request, response):
        pass

    def transform_document_pipe(self, request, response):
        pass

    def start(self):
        log.info("starting rest thread...")
        thread = Thread(
            daemon=True,
            target=waitress.serve,
            args=(self.app,),
            kwargs={"port": 8080, "_quiet": True},
        )
        thread.start()
        return thread


class DTAGrpcWorkConsumer(DTAServerServicer):
    def __init__(self, work, config) -> None:
        self._work = work
        self.config = config
        self.server = None
        super().__init__()

    def TransformDocument(
        self, request: DocumentRequest, context: ServicerContext
    ) -> TransformDocumentResponse:
        trans_document = self._work(request.document.decode())
        return TransformDocumentResponse(
            # TODO: error needs to be implemented
            trans_document=trans_document.encode("utf-8"),
            trans_output=[],
            error=[],
        )

    def ListServices(
        self, request: ListServiceRequest, context: ServicerContext
    ) -> ListServicesResponse:
        services = []
        return ListServicesResponse(services=services)

    def start(self):
        # create grpc server
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        # TODO: there is currently no case if the port is already in use
        self.server.add_insecure_port(f"[::]:{self.config.PortToListen}")
        # bind properties to be used inside the class instance
        add_DTAServerServicer_to_server(self, self.server)
        self.server.start()


protocols = {"rest": DTARestWorkConsumer, "grpc": DTAGrpcWorkConsumer}


class DTAServer(ABC):
    @abstractmethod
    def work(self, document: str) -> str:
        pass

    @classmethod
    def run(cls):
        print("execute run")
        working_home_dir = Path.home()

        # TODO: rename app_name to name
        app_name = getattr(cls, "name", "UNKNOWN")
        if app_name == "UNKNOWN":
            log.warning("no app name was specified instead using: UNKNOWN!")
        # doctrans: dts
        config = DTAServerConfig(
            app_name=app_name,
            config_file=str(
                working_home_dir / Path("/.dta/") / app_name / Path("/config.json")
            ),
            log_level="INFO",
        )

        # parse arguments to populate the configuration
        args = parser.parse_args()
        for arg in vars(args).items():
            if arg[1]:
                setattr(config, arg[0], arg[1])

        log.getLogger().setLevel(config.log_level)

        # create new config file by saving the default values
        if config.init:
            config.save()
            log.info(
                "Wrote example configuration file to {}. Exiting".format(
                    config.config_file
                )
            )
            exit(0)
            return

        # register at eureka server
        if config.register:
            eureka_client.init_registry_client(
                eureka_server=config.registrar_url,
                instance_id=config.host_name,
                app_name=config.app_name,
                instance_port=int(config.port_to_listen),
                instance_secure_port_enabled=config.is_ssl,
                # TODO: change dta type name to use the same from the rest specification
                metadata={"DTA-Type": config.dta_type},
            )

        cls_instance = cls()
        # start protocol consumer
        for protocol in args.protocols:
            instance = protocols[protocol](cls_instance.work, config)
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
            print(f" [grpc] -> listening on port {config.port_to_listen}")
            if config.rest: print(f" [rest] -> listening on port {config.http_port}")
            print("")
            print(cr.Fore.YELLOW + "     You see this message because __debug__ is true.")
            print("     Use the -O flag to enable optimization `python -O`." + cr.Fore.RESET)
            print("")
        # fmt: on

        try:
            input()
        except KeyboardInterrupt:
            pass
