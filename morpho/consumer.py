from abc import ABC, abstractmethod
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
import io
from morpho.rest.models import Health

from py_eureka_client.eureka_client import Applications
from morpho.error import NoWorkerFunctionError

from pydantic.main import BaseModel
from morpho.types import Schema, Worker, DtaType
from morpho.client import Client, ClientConfig
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
from typing import Dict, List, Optional, Tuple, Type, cast
from urllib.error import URLError
import py_eureka_client.eureka_client as eureka_client

from flask import Flask
import flask
import waitress

from morpho.rest import Status

from morpho.log import logging

log = logging.getLogger(__name__)

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
        work: Optional[Worker],
        config: "ServiceConfig",
        options_type: Optional[Type[BaseModel]],
        client: Optional[Client] = None,
    ) -> None:
        self._work = work
        self.config = config
        if client is None:
            self.client = Client(ClientConfig(registrar_url=config.registrar_url))
        else:
            self.client = client
        self.options_type = options_type
        log.info("initialized abc worker.")

    def _get_applications(self) -> Applications:
        try:
            return eureka_client.get_applications(self.config.registrar_url)
        # TODO: add custom eureka not found error
        except URLError:
            log.error("no eureka instance is running at: %s", self.config.registrar_url)
            exit(1)

    def health(self) -> Health:
        return self.config.health

    def list_services(self) -> ListServicesResponse:
        """Lists all services from the eureka server of the provided ``ServiceConfig``.
        
        Returns:
            List[ListServicesResponse]: List of services.
        """
        # return the service itself if the service is not registered at eureka
        if not self.config.should_register:
            return ListServicesResponse(
                services=[
                    ServiceInfo(name=self.config.name.upper(), options=self.options())
                ]
            )

        applications = self._get_applications()
        cached_applications: List[Tuple[str, str]] = []

        # check if we can find a available gateway
        for service in applications.applications:
            instance = service.instances[0]

            # skip self
            if instance.app == self.config.name.upper():
                continue
            instance_address = f"{instance.ipAddr}:{instance.port.port}"

            if instance.metadata:
                try:
                    dta_type = DtaType(instance.metadata.get("dtaType"))
                except ValueError:
                    dta_type = DtaType.UNKNOWN

                if dta_type == dta_type.GATEWAY:
                    log.info(
                        "found gateway send list request directly to <%s (%s)>",
                        instance.app,
                        instance_address,
                    )
                    # TODO: gateways could cache the whole list of services
                    return self.client.list_services(
                        instance.app, instance_address=instance_address
                    )

            # cache the list of instance_addresses
            cached_applications.append((instance.app, instance_address))

        services = [ServiceInfo(name=self.config.name.upper(), options=self.options())]
        # iterate over cached applications and create ListServicesResponse
        for cached_application in cached_applications:
            app_name, instance_address = cached_application
            # get options from service via rest call
            options = self.client.get_options(
                service_name=app_name, instance_address=instance_address
            )
            services.append(ServiceInfo(name=app_name, options=options))

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
                if self._work is None:
                    raise NoWorkerFunctionError("No worker function specified!")
                try:
                    if options is None:
                        document = self._work(request.document)
                    else:
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
        self,
        work: Optional[Worker],
        config: "ServiceConfig",
        options_type: Optional[Type[BaseModel]],
        client: Optional[Client] = None,
    ):
        log.info("initialized abc worker.")
        super().__init__(work, config, options_type, client)
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
        self.app.add_url_rule("/health", "health", self._health, methods=["GET"])
        # pylint: enable: line-too-long
        # fmt: on

    def _options(self) -> Tuple[Schema, Status]:
        """Callback function which gets invoked by flask if a 'options' request is received.

        Returns:
            Tuple[Schema, Status]: Returns a flask response. Returns an empty dict if the options_type is empty.
        """
        options = self.options()
        return options, Status.OK

    def _health(self) -> Tuple[Dict[str, str], Status]:
        # FIXME: pydantic does not convert Enum to string if using dict() only with json()
        health = self.health().dict()
        health["status"] = health["status"].value
        return health, Status.OK

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


@dataclass
class RestGatewayServiceConfig(ServiceConfig):
    public_ip: bool = False
    resolver_url: str = ""
    resolver_registration: bool = False


class RestGatewayConsumer(RestWorkConsumer):
    """Implements a gateway consumer on top of the rest protocol.
    """

    def __init__(
        self,
        work: Optional[Worker],
        config: ServiceConfig,
        options_type: Optional[Type[BaseModel]],
    ) -> None:
        # consumers are only invoked with ServiceConfig
        # so we need to cast to the RestGatewayServiceConfig
        super().__init__(
            work=work,
            config=config,
            options_type=options_type,
            client=Client(
                ClientConfig(
                    registrar_url=cast(RestGatewayServiceConfig, config).resolver_url
                )
            ),
        )
        # TODO: somehow remove one of the config instances
        # self.gateway_config = cast(config
        # TODO: discuss: set implicit the default type to Gateway
        self.config.type = DtaType.GATEWAY

    def _get_applications(self) -> Applications:
        applications = super()._get_applications()
        try:
            resolver_applications = eureka_client.get_applications(
                cast(RestGatewayServiceConfig, self.config).resolver_url
            )
        # TODO: add custom eureka not found error
        except URLError:
            log.error(
                "no eureka instance is running at: %s",
                cast(RestGatewayServiceConfig, self.config).resolver_url,
            )
            exit(1)

        gateway_prefix = self.config.name.split(".")[0]
        for application in resolver_applications.applications:
            application.instances[
                0
            ].app = f"{gateway_prefix}.{application.instances[0].app}"
            # application.name = "CR" + application.name
            applications.add_application(application)

        return applications

    def _transform_document(self) -> Tuple[RawTransformDocumentResponse, Status]:
        """Callback function which gets invoked by flask if a 'transform' request is received.

        Returns:
            Tuple[RawTransformDocumentResponse, Status]: Returns a flask response.
        """
        request_model = TransformDocumentRequest(**flask.request.json)
        result = self.client.transform_document(**request_model.dict())
        return cast(RawTransformDocumentResponse, result.dict()), Status.OK

    def _transform_document_pipe(
        self,
    ) -> Tuple[RawTransformDocumentPipeResponse, Status]:
        """Callback function which gets invoked by flask if a 'transform pipe' request is received.

        Returns:
            Tuple[RawTransformDocumentPipeResponse, Status]: Returns a flask response.
        """
        request_model = TransformDocumentPipeRequest(**flask.request.json)
        result = self.client.transform_document_pipe(**request_model.dict())
        return cast(RawTransformDocumentPipeResponse, result.dict()), Status.OK
