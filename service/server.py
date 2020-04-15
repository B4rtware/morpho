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
from typing import Callable, Dict, List, NewType, Optional, Tuple, TypedDict, Protocol
from urllib.error import HTTPError, URLError


import colorama as cr
import flask
from flask import Flask

# from flask_swagger_ui import get_swaggerui_blueprint
from swagger_ui import api_doc
import grpc
from grpc import ServicerContext
from py_eureka_client.eureka_client import Application, Applications
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

class RawListResponse(TypedDict):
    services: List[str]


Options = NewType("Options", Dict[str, str])
Headers = NewType("Headers", Dict[str, str])


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

# TODO: rename to Base prefix or suffix
class WorkConsumer(ABC):
    """An abstract class which must be implemented by each ``work`` consumer.

    Attributes:
        work (Callable[[str], str]): Worker function which will executed to get the
                                     transformed document.
        config (DTAServerConfig): Configuration for the given DTAServer.

    Note:
        The ``work`` callback should be called once on a implemented work consumer after the
        server received the request. After receiving the request the document should be already
        be correctly marshalled.
    """
    def __init__(self, work: Callable[[str], str], config: DTAServerConfig) -> None:
        self._work = work
        self.config = config

    def get_services(self) -> List[str]:
        """Lists all services names from the eureka server of the provided ``DTAServerConfig``.
        
        Returns:
            List[str]: List of applications.
        """
        applications = []
        if self.config.register:
            try:
                for application in eureka_client.get_applications(self.config.registrar_url).applications:
                    applications.append(application.instances[0].app)
            except URLError:
                log.error("no eureka instance is running at: {}".format(self.config.registrar_url))
        # the service always knows itsself
        if not applications:
            applications.append(self.config.app_name)
        return applications

    @abstractmethod
    def start(self) -> None:
        """starts the implemented server instance.

        Raises:
            NotImplementedError: Must be implemented on the derived class.

        Hint:
            Can be used to instantiate a new ``Thread`` for the listening server of the DTAServer.
            Creating a new Thread with ``daemon=True`` helps the thread to destroy its self 
            which will then gracefully shutdown if the DTAServer gets terminated
            (preventing zombie threads).

        Important:
            This function should not block.
        """
        raise NotImplementedError

class DTARestWorkConsumer(WorkConsumer):
    """Implements a rest work consumer server.
    
    Attributes:
        work (Callable[[str], str]): Worker function which will executed to get the
                                     transformed document.
        config (DTAServerConfig): Configuration for the given DTAServer.
    """
    def __init__(self, work: Callable[[str], str], config: DTAServerConfig):
        super().__init__(work, config)
        log.info("initializing DTARestWorkConsumer")
        self._work = work
        self.config = config
        self.thread: Optional[Thread] = None
        self.app = Flask(__name__)
        # TODO: try to use decorator route
        # fmt: off
        # pylint: disable: line-too-long
        working_dir = Path.cwd()
        config_path = working_dir / Path("./service/rest/swagger/openapi.yaml")
        api_doc(self.app, config_path=config_path, url_prefix="/info")
        self.app.add_url_rule("/v1/qds/dta/document/transform", "transform", self.transform_document, methods=["POST"])
        self.app.add_url_rule("/v1/qds/dta/service/list", "list", self.list_services, methods=["GET"])
        self.app.add_url_rule("/v1/qds/dta/document/transform-pipe", "pipe", self.transform_document_pipe)
        # pylint: enable: line-too-long
        # fmt: on

    # TODO: rename to list services / transform document and transform document pipe
    def transform_document(
        self,
    ) -> Tuple[RawTransformDocumentResponse, Status, Headers]:
        """Callback function which gets invoked by flask if a transform request is received.

        Returns:
            Tuple[RawTransformDocumentResponse, Status, Headers: [description]

        Note:
            It captures the stdandard output and standard error of the :func:`_work` function
            therefore the stdout and stderr any exception and print output can only be seen
            inside the rest response object.
        """
        trans_document = None
        # TODO: create a decorator for capturing stdout and stderr
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
            Headers({"Content-Type": "application/json"}),
        )

    def list_services(self) -> Tuple[RawListResponse, Status, Headers]:
        services = self.get_services()
        return (
            {
                "services": services
            },
            Status.OK,
            Headers({"Content-Type": "application/json"})
        )


    # TODO: create a wrapper for this function because internally it is always the same
    def transform_document_pipe(self, request, response):
        pass

    def start(self) -> None:
        """Implements the start function to start a rest server instance.
        """
        log.info("starting rest thread...")
        self.thread = Thread(
            daemon=True,
            target=waitress.serve,
            args=(self.app,),
            kwargs={"port": self.config.port_to_listen, "_quiet": True},
        )
        self.thread.start()


class DTAGrpcWorkConsumer(DTAServerServicer):
    """Implements a grpc work consumer server.

    Attributes:
        work (Callable[[str], str]): Worker function which will executed to get the
                                     transformed document.
        config (DTAServerConfig): Configuration for the given DTAServer.
    """
    def __init__(self, work: Callable[[str], str], config: DTAServerConfig) -> None:
        self._work = work
        self.config = config
        self.server = None
        super().__init__()

    def TransformDocument(
        self, request: DocumentRequest, context: ServicerContext
    ) -> TransformDocumentResponse:
        """Implements the protobuf message handler.
        
        Args:
            request (DocumentRequest): Protobuf DocumentRequest request object.
            context (ServicerContext): Protobuf ServicerContext.
        
        Returns:
            TransformDocumentResponse: Protobuf response object.
        """
        # TODO: use decorator for stdout and stderr
        trans_document = self._work(request.document.decode())
        return TransformDocumentResponse(
            # TODO: error needs to be implemented
            trans_document=trans_document.encode("utf-8"),
            trans_output=[],
            error=[],
        )

    # TODO: create a wrapper for this function because internally it is always the same
    def ListServices(
        self, request: ListServiceRequest, context: ServicerContext
    ) -> ListServicesResponse:
        services = []
        return ListServicesResponse(services=services)

    # TODO: create a wrapper for this function because internally it is always the same
    def start(self):
        """Implements the start function to start a grpc server instance.
        """
        # create grpc server
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        # TODO: there is currently no case if the port is already in use
        self.server.add_insecure_port(f"[::]:{self.config.port_to_listen}")
        # bind properties to be used inside the class instance
        add_DTAServerServicer_to_server(self, self.server)
        self.server.start()


# TODO: create base class consumer to reflect the interface
protocols = {"rest": DTARestWorkConsumer, "grpc": DTAGrpcWorkConsumer}


class DTAServer(ABC):
    """DtaServer isjdiajsdo
    """
    def __init__(self) -> None:
        self._protocols = {}

    def register_consumer(self, name: str, work_consumer: WorkConsumer):
        """Registers a work consumer.

        Args:
            name (str): The name of the consumer.
            work_consumer (WorkConsumer): A class which implements :class:`WorkConsumer`.
        """
        self._protocols[name] = work_consumer

    def remove_consumer(self, name: str):
        """Removes a work consumer.

        Args:
            name (str): The name of the consumer which will be removed.
        """
        del self._protocols[name]

    @abstractmethod
    def work(self, document: str) -> str:
        """This is an abstract worker function which must be implemented on its derived class.

        Args:
            document (str): The document in plain text.

        Returns:
            str: The transformed document in plain text.

        Raises:
            NotImplementedError: Must be implemented in derived class.
        """
        raise NotImplementedError()

    @classmethod
    def run(cls):
        """Class method which is used to invoke the server.
        """
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
        assert cls_instance._protocols, "Have you called super() on your DTAServer implemenation?"
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


def run_app(cls: DTAServer):
    """Decorator to apply on the microservice app class which will be then automatically run.

    Args:
        cls (DTAServer): Class object of the decorated DTAServer implementation.
    """
    cls.run()
