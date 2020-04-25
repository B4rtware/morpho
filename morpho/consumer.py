from abc import ABC, abstractmethod
from contextlib import redirect_stderr, redirect_stdout
import io
from threading import Thread
import traceback
from typing import Callable, List, Optional, Tuple
from urllib.error import URLError

from flask import Flask
import flask
import waitress

from morpho.config import ServerConfig
from morpho.log import log
from morpho.rest import Status
from morpho.types import (
    Headers,
    RawListResponse,
    RawServiceInfo,
    RawTransformDocumentResponse,
)

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
            # TODO: add custom eureka not found error
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

        error = captured_stderr.getvalue().splitlines()
        trans_output = captured_stdout.getvalue().splitlines()
        captured_stderr.close()
        captured_stdout.close()
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


# class GrpcWorkConsumer(DTAServerServicer):
#     """Implements a grpc work consumer server.

#     Attributes:
#         work (Callable[[str], str]): Worker function which will executed to get the
#                                      transformed document.
#         config (ServerConfig): Configuration for the given Server.
#     """

#     def __init__(self, work: Callable[[str], str], config: ServerConfig) -> None:
#         self._work = work
#         self.config = config
#         self.server = None
#         super().__init__()

#     def TransformDocument(
#         self, request: DocumentRequest, context: ServicerContext
#     ) -> TransformDocumentResponse:
#         """Implements the protobuf message handler.

#         Args:
#             request (DocumentRequest): Protobuf DocumentRequest request object.
#             context (ServicerContext): Protobuf ServicerContext.

#         Returns:
#             TransformDocumentResponse: Protobuf response object.
#         """
#         # TODO: use decorator for stdout and stderr
#         trans_document = self._work(request.document.decode())
#         return TransformDocumentResponse(
#             # TODO: error needs to be implemented
#             trans_document=trans_document.encode("utf-8"),
#             trans_output=[],
#             error=[],
#         )

#     # TODO: create a wrapper for this function because internally it is always the same
#     def ListServices(
#         self, request: ListServiceRequest, context: ServicerContext
#     ) -> ListServicesResponse:
#         services = []
#         return ListServicesResponse(services=services)

#     # TODO: create a wrapper for this function because internally it is always the same
#     def start(self):
#         """Implements the start function to start a grpc server instance.
#         """
#         # create grpc server
#         self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#         # TODO: there is currently no case if the port is already in use
#         self.server.add_insecure_port(f"[::]:{self.config.port_to_listen}")
#         # bind properties to be used inside the class instance
#         add_DTAServerServicer_to_server(self, self.server)
#         self.server.start()
