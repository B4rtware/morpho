from abc import ABC, abstractmethod
from base64 import b64decode, b64encode
import binascii
from dataclasses import dataclass
import json
from morpho.types import Options
# from morpho.config import BaseConfig
import morpho.config as config
from typing import Any, Dict, List, Optional, TypedDict

# from morpho.types import (
#     Options,
#     RawListServicesResponse,
#     RawServiceInfo,
#     RawTransformDocumentPipeRequest,
#     RawTransformDocumentPipeResponse,
#     RawTransformDocumentRequest,
#     RawTransformDocumentResponse,
# )

def _encode_base64(string: str, encoding: str = "utf-8"):
    return b64encode(string.encode(encoding)).decode(encoding)

def _decode_base64(string: str, encoding: str = "utf-8"):
    return b64decode(string.encode(encoding)).decode(encoding)

# +-------------------------------------------------------------------------------------+
# |                                  Raw Dict Types                                     |
# +-------------------------------------------------------------------------------------+

# consider to mvoe this into types again (or are they RawTypeModels?)

class RawTransformDocumentResponse(TypedDict):
    """Raw TransformDocumentResponse dict type"""

    document: str
    output: Optional[List[str]]
    error: Optional[List[str]]


class RawTransformDocumentRequest(TypedDict):
    """Raw TransformDocumentRequest dict type"""

    document: str
    service_name: str
    file_name: Optional[str]
    options: Optional[Options]

# class RawListService(TypedDict):
#     """Raw ListService dict type"""

#     name: str
#     version: str
#     options: Dict[str, Any]


class RawServiceInfo(TypedDict):
    """Raw ServiceInfo dict type"""

    name: str
    version: str
    options: Optional[Dict[str, Any]]


class RawListServicesResponse(TypedDict):
    """Raw ListResponse dict type"""

    services: List[RawServiceInfo]


class RawTransformDocumentPipeRequest(TypedDict):
    """Raw TransformDocumentPipeRequest dict type"""

    document: str
    file_name: Optional[str]
    services: List[RawServiceInfo]


class RawTransformDocumentPipeResponse(RawTransformDocumentResponse):
    """Raw TransformDocumentPipeResponse dict type"""

    sender: str

# its models raw responses

# TODO: remove boilerplate code
# TODO: consider to create a warning if the document is empty

# TODO: consider to use a normal class here insteat of dataclasses because of the weird issure with intellisense
# TODO: consider to use a dataclasses if the problem is solved with having a dataclass and properties


class BaseModel(ABC):
    @abstractmethod
    def as_dict(self) -> Any:
        pass

    def as_json(self, indent: Optional[int] = None) -> str:
        """Creates a serialized json string from the object instance.

        Returns:
            str: A json string.
        """
        return json.dumps(self.as_dict(), indent=indent)

class B64DocumentField():

    def __init__(self, document: str):
        self._document = ""
        self.document = document

    @property
    def document(self) -> str:
        return _decode_base64(self._document)

    @document.setter
    def document(self, document: str):
        self._document = _encode_base64(self._document)
    

class TransformDocumentRequest(BaseModel, B64DocumentField):
    def __init__(
        self,
        document: str,
        service_name: str,
        file_name: Optional[str] = None,
        options: Optional[Options] = None,
    ) -> None:
        super().__init__(document=document)
        self.service_name = service_name
        self.file_name = file_name
        self.options = options

    def as_dict(self) -> RawTransformDocumentRequest:
        """Creates a dict of the object instance.

        Returns:
            RawTransformDocumentResponse: TransformDocumentResponse as dict.
        """
        return RawTransformDocumentRequest(
            document=self.document,
            service_name=self.service_name,
            file_name=self.file_name,
            options=self.options,
        )

# TODO: abstract it to a document variable which is inside another class so the validation process is only on one instance?
class TransformDocumentResponse(BaseModel, B64DocumentField):
    def __init__(
        self,
        document: str,
        output: Optional[List[str]] = None,
        error: Optional[List[str]] = None,
    ) -> None:
        super().__init__(document=document)
        self.output = output
        self.error = error

    def as_dict(self) -> RawTransformDocumentResponse:
        """Creates a dict of the object instance.

        Returns:
            RawTransformDocumentResponse: TransformDocumentResponse as dict.
        """
        return RawTransformDocumentResponse(
            document=self.document,
            output=self.output,
            error=self.error,
        )

@dataclass
class ServiceInfo(BaseModel):
    name: str
    version: str
    options: Optional[config.BaseConfig] = None

    def as_dict(self) -> RawServiceInfo:
        """Creates a dict of the object instance.

        Returns:
            RawServiceInfo: ServiceInfo as dict.
        """
        options = self.options.as_dict() if self.options else None
        return RawServiceInfo(
            name=self.name,
            version=self.version,
            options=options
        )

@dataclass
class ListServicesResponse(BaseModel):
    services: List[ServiceInfo]

    def as_dict(self) -> RawListServicesResponse:
        """Creates a dict of the object instance.

        Returns:
            RawListResponse: ListServicesResponse as dict.
        """
        return RawListServicesResponse(
            services=[service.as_dict() for service in self.services]
        )


# TODO: implement base64 encode decode
class TransformDocumentPipeRequest(BaseModel, B64DocumentField):
    def __init__(self, document: str, services: List[ServiceInfo], file_name: Optional[str]) -> None:
        super().__init__(document=document)
        self.services = services
        self.file_name = file_name

    def as_dict(self) -> RawTransformDocumentPipeRequest:
        return RawTransformDocumentPipeRequest(
            document=self.document,
            file_name=self.file_name,
            services=[info.as_dict() for info in self.services],
        )


class TransformDocumentPipeResponse(TransformDocumentResponse):
    def __init__(
        self,
        document: str,
        sender: str,
        output: Optional[List[str]] = None,
        error: Optional[List[str]] = None,
    ):
        super().__init__(
            document=document, output=output, error=error
        )
        self.sender = sender

    def as_dict(self) -> RawTransformDocumentPipeResponse:
        return RawTransformDocumentPipeResponse(
            document=self.document,
            sender=self.sender,
            output=self.output,
            error=self.error,
        )
