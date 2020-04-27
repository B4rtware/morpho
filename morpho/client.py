from base64 import b64decode, b64encode
from dataclasses import dataclass
from morpho.rest.models import ServiceInfo, TransformDocumentPipeRequest, TransformDocumentPipeResponse
from typing import List, Optional
from urllib.error import HTTPError

from py_eureka_client import eureka_client
from py_eureka_client.eureka_client import Application
import requests

from morpho.error import ServiceNotFoundError
from morpho.types import Options


@dataclass
class ClientConfig:
    registrar_url: str

# TODO: consider to use models instead of function arguments e.g TransformDocumentRequest
class Client:
    def __init__(self, config: ClientConfig) -> None:
        self.config = config

    def _get_instance_ip_address(self, service_name: str) -> Optional[str]:
        service: Optional[Application] = None
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
            return f"{instance.ipAddr}:{instance.port.port}"
        return None

    # TODO: consider to use **kwargs for options
    def transform_document(
        self,
        document: str,
        service_name: str,
        options: Optional[Options] = None,
        file_name: Optional[str] = None,
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
        # get application from eureka
        instance_address = self._get_instance_ip_address(service_name)
        if instance_address:
            # wrapper for a consumer request
            response = requests.post(
                f"http://{instance_address}/v1/qds/dta/document/transform",
                json={
                    "document": b64encode(document.encode("utf-8")).decode("utf-8"),
                    "file_name": file_name,
                    "service_name": service_name,
                },
            )
            response_object = response.json()
            response_object["trans_document"] = b64decode(
                response_object["trans_document"].encode("utf-8")
            ).decode("utf-8")
            return response_object

    def transform_document_pipe(self, request: TransformDocumentPipeRequest) -> TransformDocumentPipeResponse:
        # TODO: 
        instance_address = self._get_instance_ip_address(request.services[0].name)
        print(request.as_dict())
        if instance_address:
            response = requests.post(
                f"http://{instance_address}/v1/qds/dta/document/transform-pipe",
                json=request.as_dict()
            )
            print(response.text)
            return TransformDocumentPipeResponse(**response.json())

    def list_services(self, service_name: str) -> List[str]:
        """Lists the services which are known by the provided service.
        
        Args:
            service_name (str): Service name.
        
        Returns:
            List[str]: List of known service names.

        Note:
            Will always return its own service name.
        """
        instance_address = self._get_instance_ip_address(service_name)
        if instance_address:
            response = requests.get(
                f"http://{instance_address}/v1/qds/dta/service/list"
            )
            response_object = response.json()
            return response_object["services"]
        return []


if __name__ == "__main__":
    config = ClientConfig(registrar_url="http://localhost:8761/eureka")
    morpho_client = Client(config)
    # document = morpho_client.transform_document(
    #     "Test Dokument", "DE.TU-BERLIN.QDS.ECHO", file_name="file.txt"
    # )
    # print(c.list_services("DE.TU-BERLIN.QDS.ECHO"))
    # print(document["trans_document"])

    request = TransformDocumentPipeRequest(
        document="Hello World",
        file_name=None,
        services=[
            ServiceInfo(name="DE.TU-BERLIN.QDS.ECHOS", version="0.0.1", options=None),
            ServiceInfo(name="DE.TU-BERLIN.QDS.ECHOS2", version="0.0.1", options=None),
            ServiceInfo(name="DE.TU-BERLIN.QDS.ECHOS3", version="0.0.1", options=None)
        ]
    )
    morpho_client.transform_document_pipe(request=request)
