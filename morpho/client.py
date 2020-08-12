from dataclasses import dataclass

from pydantic.main import BaseModel
from morpho.rest.models import (
    TransformDocumentPipeRequest,
    TransformDocumentPipeResponse,
    TransformDocumentRequest,
    TransformDocumentResponse,
)
from typing import List, Optional
from urllib.error import HTTPError

from py_eureka_client import eureka_client
from py_eureka_client.eureka_client import Application
import requests

from morpho.error import ServiceNotFoundError

# from morpho.log import log
# import logginga

from morpho.log import logging

log = logging.getLogger(__name__)


@dataclass
class ClientConfig:
    registrar_url: str


# TODO: consider to use models instead of function arguments e.g TransformDocumentRequest
# TODO: add requests parameter such as headers cookies etc which then also can be used on service
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
                    "found instance: <%s> at <%s:%s>", instance.app, instance.ipAddr, instance.port.port
                )
            return f"{instance.ipAddr}:{instance.port.port}"
        return None

    # TODO: consider to use **kwargs for options
    def transform_document(
        self,
        document: str,
        service_name: str,
        options: Optional[BaseModel] = None,
        file_name: Optional[str] = None,
        address: Optional[str] = None,
    ):
        """Transforms the given document.
        
        Args:
            document (str): Document to be transformed.
            file_name (str): Filename of the document.
            service_name (str): Service name for the requested service.
            options (Optional[Options], optional): Service specific options. Defaults to None.
        
        Raises:
            ServiceNotFoundError: If the requested service in the eureka registry could not be found.
        """
        request = TransformDocumentRequest(
            document=document,
            service_name=service_name,
            file_name=file_name,
            options=options,
        )
        # get application from eureka
        if address is None:
            address = f"http://{self._get_instance_ip_address(service_name)}/v1/document/transform"
        if address:
            # wrapper for a consumer request
            log.info("sending <DocumentTransformRequest> to <%s>", address)
            log.info("content: %s", request.json(indent=4))
            response = requests.post(address, json=request.dict())
            # TODO: if url not found json object not available return error
            log.debug("content of response: %s", response.text)
            response_object = TransformDocumentResponse(**response.json())
            return response_object

    def transform_document_pipe(
        self, request: TransformDocumentPipeRequest
    ) -> TransformDocumentPipeResponse:
        instance_address = self._get_instance_ip_address(request.services[0].name)
        # print(request.as_dict())
        if instance_address is None:
            message = f"No service named <{request.services[0].name}>."
            raise ServiceNotFoundError(message)
        log.info("sending transform document pipe request.")
        log.info("content: %s", request.json(indent=4))
        response = requests.post(
            f"http://{instance_address}/v1/document/transform-pipe",
            json=request.dict(),
        )
        # print(response.text)
        return TransformDocumentPipeResponse(**response.json())

    def list_services(self, service_name: Optional[str]) -> List[str]:
        """Lists the services which are known by the provided service.
        
        Args:
            service_name (str): Service name.
        
        Returns:
            List[str]: List of known service names.

        Note:
            Will always return its own service name.
        """
        if not service_name:
            instance_address = self._get_instance_ip_address(service_name)
        if instance_address:
            response = requests.get(f"http://{instance_address}/v1/service/list")
            response_object = response.json()
            return response_object["services"]
        return []


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
