from abc import ABC, abstractmethod
from contextlib import redirect_stderr, redirect_stdout
import io

from pydantic.main import BaseModel
from morpho.types import Schema, Worker
from morpho.client import Client, ClientConfig
from morpho.util import unflatten_dict
from morpho.rest.models import (
    ListServicesResponse,
    PipeService,
    ServiceInfo,
    TransformDocumentPipeRequest,
    TransformDocumentPipeResponse,
    TransformDocumentRequest,
    TransformDocumentResponse,
)
from morpho.rest.raw import (
    RawTransformDocumentPipeResponse,
    RawTransformDocumentResponse,
    RawListServicesResponse,
)
from threading import Thread
import traceback
from typing import Optional, TYPE_CHECKING, Tuple, Type
from urllib.error import URLError
import py_eureka_client.eureka_client as eureka_client

from flask import Flask
import flask
import waitress

from morpho.rest import Status

from morpho.log import logging

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from morpho.config import ServiceConfig

# TODO: rename to Base prefix or suffix
class WorkConsumer(ABC):
    """An abstract class which must be implemented by each ``work`` consumer.

    Attributes:
        work (Callable[[str], str]): Worker function which will executed to get the
                                     transformed document.
        config (ServiceConfig): Configuration for the given Server.

    Note:
        The ``work`` callback should be called once on a implemented work consumer after the
        server received the request. After receiving the request the document should be already
        be correctly marshalled.
    """

    def __init__(
        self,
        work: Worker,
        config: "ServiceConfig",
        options_type: Optional[Type[BaseModel]],
    ) -> None:
        self._work = work
        self.config = config
        self.client = Client(ClientConfig(registrar_url=config.registrar_url))
        self.options_type = options_type
        log.info("initialized abc worker.")

    def list_services(self) -> ListServicesResponse:
        """Lists all services from the eureka server of the provided ``ServiceConfig``.
        
        Returns:
            List[ListServicesResponse]: List of services.
        """
        services = []
        if self.config.register:
            try:
                applications = eureka_client.get_applications(self.config.registrar_url)
                for service in applications.applications:
                    instance = service.instances[0]
                    service_info = ServiceInfo(name=instance.app)
                    services.append(service_info)
            # TODO: add custom eureka not found error
            except URLError:
                log.error(
                    "no eureka instance is running at: %s", self.config.registrar_url
                )
        # the service always knows its self
        if not services:
            services.append(ServiceInfo(name=self.config.name,))
        return ListServicesResponse(services=services)

    def options(self) -> Schema:
        """Lists available options of the service.

        Returns:
            Schema: A Schema representing the different available options. Returns an empty dictionary `{}` if no option is present.
        """
        if self.options_type is None:
            return {}
        return self.options_type.schema()

    def transform_document(
        self, request: TransformDocumentRequest,
    ) -> TransformDocumentResponse:
        document = None
        # TODO: create a decorator for capturing stdout and stderr
        # TODO: consider to move this into base class
        captured_stdout = io.StringIO()
        captured_stderr = io.StringIO()
        with redirect_stderr(captured_stderr):
            with redirect_stdout(captured_stdout):
                options = (
                    self.options_type(**request.options) if self.options_type else None
                )
                try:
                    document = self._work(request.document, options)
                except BaseException:  # pylint: disable=broad-except
                    traceback.print_exc()
        error = captured_stderr.getvalue().splitlines()
        output = captured_stdout.getvalue().splitlines()
        captured_stderr.close()
        captured_stdout.close()
        log.info("-- after transform document --")
        log.info("document: %s", document)
        log.info("error: %s", error)
        log.info("output: %s", output)
        # TODO: test on none return type (if an error occurs) so the error
        # will be still be transferred to the client
        return TransformDocumentResponse(document=document, output=output, error=error)

    def transform_document_pipe(
        self, request: TransformDocumentPipeRequest
    ) -> TransformDocumentPipeResponse:
        log.info("transform document pipe was called with: <%s>", request.document)
        pipe_service = request.services.pop(0)
        transform_response = self.transform_document(
            TransformDocumentRequest(
                document=request.document,
                service_name=pipe_service.name,
                file_name=request.file_name,
                options=pipe_service.options,
            )
        )
        # return a response if there are only 1 service left
        # this means that the pipe is either finished or will
        # be interupted because of an occured error
        if request.services == [] or transform_response.error:
            log.info(
                "reached end of pipe returning response: %s",
                transform_response.document,
            )
            return TransformDocumentPipeResponse(
                document=transform_response.document,
                output=transform_response.output,
                last_transformer=self.config.name,
                error=transform_response.error,
            )

        request.document = transform_response.document
        response = self.client.transform_document_pipe(request=request)

        # cancat outputs in the right order
        response.output = transform_response.output + response.output
        response.error = transform_response.error + response.error

        return response

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
        config (ServiceConfig): Configuration for the given Server.
    """

    def __init__(
        self, work: Worker, config: "ServiceConfig", options_type: Type[BaseModel]
    ):
        log.info("initialized abc worker.")
        super().__init__(work, config, options_type)
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
        self.app.add_url_rule("/v1/service/options", "options", self._options, methods=["GET"])
        self.app.add_url_rule("/v1/service/list", "list", self._list_services, methods=["GET"])
        self.app.add_url_rule("/v1/document/transform", "transform", self._transform_document, methods=["POST"])
        self.app.add_url_rule("/v1/document/transform-pipe", "pipe", self._transform_document_pipe, methods=["POST"])
        # pylint: enable: line-too-long
        # fmt: on

    def _options(self) -> Tuple[Schema, Status]:
        """Callback function which gets invoked by flask if a 'options' request is received.

        Returns:
            Tuple[Schema, Status]: Returns a flask response. Returns an empty dict if the options_type is empty.
        """
        options = self.options()
        return options, Status.OK

    # TODO: rename to list services / transform document and transform document pipe
    def _transform_document(self) -> Tuple[RawTransformDocumentResponse, Status]:
        """Callback function which gets invoked by flask if a 'transform' request is received.

        Returns:
            Tuple[RawTransformDocumentResponse, Status]: Returns a flask response.

        Note:
            It captures the standard output and standard error of the :func:`_work` function
            therefore the stdout and stderr any exception and print output can only be seen
            inside the rest response object.
        """
        # TODO: what if body is empty -> test
        log.info("received request on rest worker")
        log.debug("content received: %s", flask.request.json)
        request_model = TransformDocumentRequest(**flask.request.json)
        response_model = self.transform_document(request_model)
        status_code = (
            Status.OK if not response_model.error else Status.INTERNAL_SERVER_ERROR
        )
        return response_model.dict(), status_code

    # TODO: add options to the list reponse for each application maybe on /options or so
    # TODO: or override and call super() ?
    def _list_services(self) -> Tuple[RawListServicesResponse, Status]:
        """Callback function which gets invoked by flask if a 'list' request is received.

        Returns:
            Tuple[RawListServicesResponse, Status]: Returns a flask response.
        """
        response_model = self.list_services()
        return response_model.dict(), Status.OK

    # TODO: create a wrapper for this function because internally it is always the same
    # TODO: consider to rename this function to _transform_document_pipe to call a super function
    # TODO: which get called with the TransformDocumentPipeRequest model
    # TODO: is it possible to use **request even ServiceInfo is required on services?
    def _transform_document_pipe(
        self,
    ) -> Tuple[RawTransformDocumentPipeResponse, Status]:
        """Callback function which gets invoked by flask if a 'transform pipe' request is received.

        Returns:
            Tuple[RawTransformDocumentPipeResponse, Status]: Returns a flask response.
        """
        request = flask.request.json
        request_model = TransformDocumentPipeRequest(
            document=request["document"],
            file_name=request["file_name"],
            services=[PipeService(**info) for info in request["services"]],
        )
        response_model = self.transform_document_pipe(request_model)
        status_code = (
            Status.OK if not response_model.error else Status.INTERNAL_SERVER_ERROR
        )
        return response_model.dict(), status_code

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
