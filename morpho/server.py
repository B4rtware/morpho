""" This module contains the server which implements the base functionality for a service.

It also contains the raw responses and request types.

Warning:
    This might change in future versions.
"""
from abc import ABC, abstractmethod
import argparse
import concurrent.futures as futures
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
import dataclasses
from enum import Enum
import io
from pathlib import Path
import sys
from threading import Event, Thread
import traceback
from typing import Any, Callable, Dict, List, NewType, Optional, Tuple, TypedDict
from urllib.error import URLError

import colorama as cr
import flask
from flask import Flask
import grpc
from grpc import ServicerContext
import py_eureka_client.eureka_client as eureka_client
import waitress

from morpho.config import ServerConfig
from morpho.log import log
from morpho.proto.dtaservice_pb2 import DocumentRequest, TransformDocumentResponse
from morpho.proto.dtaservice_pb2 import ListServicesResponse
from morpho.proto.dtaservice_pb2 import ListServiceRequest
from morpho.proto.grpc.dtaservice_pb2_grpc import add_DTAServerServicer_to_server
from morpho.proto.grpc.dtaservice_pb2_grpc import DTAServerServicer
from morpho.rest import Status


cr.init()

Options = NewType("Options", Dict[str, Any])
Headers = NewType("Headers", Dict[str, str])


class RawTransformDocumentResponse(TypedDict):
    """Raw TransformDocumentResponse dict type"""

    trans_document: Optional[str]
    trans_output: Optional[List[str]]
    error: Optional[List[str]]


class RawTransformDocumentRequest(TypedDict):
    """Raw TransformDocumentRequest dict type"""

    document: str
    service_name: str
    file_name: Optional[str]
    options: Optional[Options]


class RawListService(TypedDict):
    """Raw ListService dict type"""

    name: str
    options: Dict[str, Any]


class RawServiceInfo(TypedDict):
    """Raw ServiceInfo dict type"""

    name: str
    version: str
    options: Optional[Dict[str, Any]]


class RawListResponse(TypedDict):
    """Raw ListResponse dict type"""

    services: List[RawListService]


class RawTransformDocumentPipeRequest(RawTransformDocumentRequest):
    """Raw TransformDocumentPipeRequest dict type"""

    services: List[Dict[str, Any]]


class RawTransformDocumentPipeResponse(RawTransformDocumentResponse):
    """Raw TransformDocumentPipeResponse dict type"""

    sender: str


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
parser.add_argument("--type", type=str, help="One of Gateway or Service. Service is assumed if not provided.")
parser.add_argument("--is-ssl", type=str, help="Can the service be reached via SSL.")
parser.add_argument("--rest", action="store_true", help="REST-API enabled on port 80, if set.")
parser.add_argument("--http-port", type=str, help="On which httpPort to listen for REST, if enableREST is set. Ignored otherwise.")
parser.add_argument("--protocols", type=str, nargs='+', help="Which protocol should be used by the server.", default=["rest"], choices=("rest", "grpc"))

parser.add_argument_group("Generic")
parser.add_argument("--log-level", type=str, help="Log level, one of panic, fatal, error, warn or warning, info, debug, trace", default="INFO", choices=("CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"))
parser.add_argument("--config-file", type=str, help="The config file to use")
parser.add_argument("--init", help="Create a default config file as defined by cfg-file, if set. If not set ~/.morpho/<AppName>/config.json will be created.", action="store_true")
# pylint: enable=line-too-long
# fmt: on


# TODO: rename to Base prefix or suffix
class WorkConsumer(ABC):
    """An abstract class which must be implemented by each ``work`` consumer.

    Attributes:
        work (Callable[[str], str]): Worker function which will executed to get the
                                     transformed document.
        config (ServerConfig): Configuration for the given Server.

    Note:
        The ``work`` callback should be called once on a implemented work consumer after the
        server received the request. After receiving the request the document should be already
        be correctly marshalled.
    """

    def __init__(self, work: Callable[[str], str], config: ServerConfig) -> None:
        self._work = work
        self.config = config

    def get_services(self) -> List[RawServiceInfo]:
        """Lists all services names from the eureka server of the provided ``ServerConfig``.
        
        Returns:
            List[str]: List of applications.
        """
        applications = []
        if self.config.register:
            try:
                for application in eureka_client.get_applications(
                    self.config.registrar_url
                ).applications:
                    applications.append(application.instances[0].app)
            except URLError:
                log.error(
                    "no eureka instance is running at: {}".format(
                        self.config.registrar_url
                    )
                )
        # the service always knows its self
        if not applications:
            applications.append(
                RawServiceInfo(
                    name=self.config.app_name,
                    version=self.config.version,
                    options=self.config.options.as_dict()
                    if self.config.options
                    else None,
                )
            )
        return applications

    @abstractmethod
    def start(self) -> None:
        """starts the implemented server instance.

        Raises:
            NotImplementedError: Must be implemented on the derived class.

        Hint:
            Can be used to instantiate a new ``Thread`` for the listening server of the Server.
            Creating a new Thread with ``daemon=True`` helps the thread to destroy its self 
            which will then gracefully shutdown if the Server gets terminated
            (preventing zombie threads).

        Important:
            This function should not block.
        """
        raise NotImplementedError


class RestWorkConsumer(WorkConsumer):
    """Implements a rest work consumer server.
    
    Attributes:
        work (Callable[[str], str]): Worker function which will executed to get the
                                     transformed document.
        config (ServerConfig): Configuration for the given Server.
    """

    def __init__(self, work: Callable[[str], str], config: ServerConfig):
        super().__init__(work, config)
        self._work = work
        self.config = config
        self.thread: Optional[Thread] = None
        self.app = Flask(__name__)
        self.app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
        # TODO: try to use decorator route
        # fmt: off
        # pylint: disable: line-too-long
        # working_dir = Path.cwd()
        # config_path = working_dir / Path("./service/rest/swagger/openapi.yaml")
        # api_doc(self.app, config_path=config_path, url_prefix="/info")
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
            It captures the standard output and standard error of the :func:`_work` function
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
                    trans_document = self._work(flask.request.json["document"])
                except BaseException:  # pylint: disable=broad-except
                    traceback.print_exc()

        error = captured_stderr.readlines()
        trans_output = captured_stdout.readlines()

        return (
            {
                "trans_document": trans_document,
                "trans_output": trans_output,
                "error": error,
            },
            Status.OK if not error else Status.INTERNAL_SERVER_ERROR,
            Headers({"Content-Type": "application/json"}),
        )

    # TODO: add options to the list reponse for each application maybe on /options or so
    def list_services(self) -> Tuple[RawListResponse, Status, Headers]:
        services = self.get_services()
        return (
            {"services": services},
            Status.OK,
            Headers({"Content-Type": "application/json"}),
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
            kwargs={
                "port": self.config.port_to_listen,
                "_quiet": True,
                "clear_untrusted_proxy_headers": True,
            },
        )
        self.thread.start()


class GrpcWorkConsumer(DTAServerServicer):
    """Implements a grpc work consumer server.

    Attributes:
        work (Callable[[str], str]): Worker function which will executed to get the
                                     transformed document.
        config (ServerConfig): Configuration for the given Server.
    """

    def __init__(self, work: Callable[[str], str], config: ServerConfig) -> None:
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
protocols = {"rest": RestWorkConsumer, "grpc": GrpcWorkConsumer}


class Server(ABC):
    """Server

    Note:
        Ideally every Server should implement a debug option.
        Which will sets the log level to debug if true.
    """

    def __init__(self) -> None:
        self._protocols = {}
        self.should_stop = Event()

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
        version = getattr(cls, "version", None)
        app_name = getattr(cls, "name", "UNKNOWN")
        options = getattr(cls, "options", None)

        if app_name == "UNKNOWN":
            log.warning("no application name was specified instead using: UNKNOWN!")
        # doctrans: dts
        config = ServerConfig(
            app_name=app_name,
            version=version,
            options=options,
            config_file=str(
                working_home_dir / Path("/.morpho/") / app_name / Path("/config.json")
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
                # TODO: change morpho type name to use the same from the rest specification
                metadata={},
            )

        cls_instance = cls()
        assert (
            cls_instance._protocols
        ), "Have you called super() on your Server implemenation?"
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
            while not cls_instance.should_stop.is_set():
                cls_instance.should_stop.wait(0.5)
        except KeyboardInterrupt:
            sys.exit(0)


def run_app(cls: Server):
    """Decorator to apply on the microservice app class which will be then automatically run.

    Args:
        cls (Server): Class object of the decorated Server implementation.
    """
    cls.run()