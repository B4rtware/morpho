from dataclasses import dataclass
from typing import Optional, cast
from urllib.error import HTTPError

import requests
from py_eureka_client import eureka_client
from py_eureka_client.eureka_client import Application

from morpho.error import ServiceNotFoundError
from morpho.log import logging
from morpho.rest.models import (
    ListServicesResponse,
    TransformDocumentPipeRequest,
    TransformDocumentPipeResponse,
    TransformDocumentRequest,
    TransformDocumentResponse,
)
from morpho.types import Schema

log = logging.getLogger(__name__)

@dataclass
class ClientConfig:
    registrar_url: str


# TODO: consider to use models instead of function arguments e.g TransformDocumentRequest
# TODO: add requests parameter such as headers cookies etc which then also can be used on service
# TODO: consider to allow empty config because of the explicit instance_address parameter on each function
class Client:
    def __init__(self, config: ClientConfig) -> None:
        self.config = config

    def _get_instance_ip_address(self, service_name: str) -> Optional[str]:
        service: Optional[Application] = None
        log.info("contacting eureka at <%s>", self.config.registrar_url)
        try:
            service = eureka_client.get_application(
                self.config.registrar_url, service_name
            )
        except HTTPError as e:
            if e.code == 404:
                message = f"No service named <{service_name}>."
                # log.info(message)
                raise ServiceNotFoundError(message)

        if service:
            instance = service.instances[0]
            log.info(
                "found instance: <%s> at <%s:%s>",
                instance.app,
                instance.ipAddr,
                instance.port.port,
            )
            return f"{instance.ipAddr}:{instance.port.port}"
        return None

    def transform_document(
        self, request: TransformDocumentRequest, instance_address: Optional[str] = None,
    ) -> TransformDocumentResponse:
        """Transforms the given document.
        
        Args:
            request (TransformDocumentRequest): Request object.
            instance_address (Optional[str]): 
        
        Raises:
            ServiceNotFoundError: If the requested service in the eureka registry could not be found.
        """
        # get application from eureka
        if not instance_address:
            instance_address = self._get_instance_ip_address(request.service_name)

        # wrapper for a consumer request
        log.info("sending <DocumentTransformRequest> to <%s>", instance_address)
        log.info("content: %s", request.json(indent=4))
        response = requests.post(
            f"http://{instance_address}/v1/document/transform", json=request.dict()
        )
        # TODO: if url not found json object not available return error
        log.debug("content of response: %s", response.text)
        response_object = TransformDocumentResponse(**response.json())
        return response_object

    def transform_document_pipe(
        self,
        request: TransformDocumentPipeRequest,
        instance_address: Optional[str] = None,
    ) -> TransformDocumentPipeResponse:
        if instance_address is None:
            instance_address = self._get_instance_ip_address(request.services[0].name)
        log.info("sending transform document pipe request.")
        log.info("content: %s", request.json(indent=4))
        response = requests.post(
            f"http://{instance_address}/v1/document/transform-pipe",
            json=request.dict(),
        )
        # print(response.text)
        return TransformDocumentPipeResponse(**response.json())

    def list_services(
        self, service_name: str, instance_address: Optional[str] = None
    ) -> ListServicesResponse:
        """Lists the services which are known by the provided service.
        
        Args:
            service_name (str): Service name.
        
        Returns:
            List[str]: List of known service names.

        Note:
            Will always return its own service name.
        """
        if not instance_address:
            instance_address = self._get_instance_ip_address(service_name)

        response = requests.get(f"http://{instance_address}/v1/service/list")
        # FIXME: missing validation (try except)
        return ListServicesResponse(**response.json())

    def get_options(
        self, service_name: str, instance_address: Optional[str] = None
    ) -> Schema:
        if instance_address is None:
            instance_address = self._get_instance_ip_address(service_name)

        response = requests.get(f"http://{instance_address}/v1/service/options")
        return cast(Schema, response.json())


# if __name__ == "__main__":
#     config = ClientConfig(registrar_url="http://localhost:8761/eureka")
#     morpho_client = Client(config)
#     document = morpho_client.transform_document(
#         "Test Dokument", "PROXY", file_name="file.txt"
#     )
# print(document)
# print(c.list_services("DE.TU-BERLIN.QDS.ECHO"))
# print(document["trans_document"])

# request = TransformDocumentPipeRequest(
#     document="Hello World",
#     file_name=None,
#     services=[
#         ServiceInfo(name="DE.TU-BERLIN.QDS.ECHOS", version="0.0.1", options=None),
#         ServiceInfo(name="DE.TU-BERLIN.QDS.ECHOS2", version="0.0.1", options=None),
#         ServiceInfo(name="DE.TU-BERLIN.QDS.ECHOS3", version="0.0.1", options=None)
#     ]
# )
# morpho_client.transform_document_pipe(request=request)
