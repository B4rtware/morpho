from abc import ABC, abstractmethod
import binascii
from dataclasses import dataclass
import json
from morpho.util import decode_base64, encode_base64
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

# +-------------------------------------------------------------------------------------+
# |                                  Raw Dict Types                                     |
# +-------------------------------------------------------------------------------------+

# TODO: consider to mvoe this into types again (or are they RawTypeModels?)


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

    last_transformer: str


class RawPipeService(TypedDict):
    name: str
    options: Options


class RawOptionsPropertyError(TypedDict):
    name: str
    message: str


class RawOptionsErrorResponse(TypedDict):
    code: int
    properties: List[RawOptionsPropertyError]


class RawErrorResponse(TypedDict):
    code: int
    message: str


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


class B64DocumentField:
    def __init__(self, document: str, is_base64_encoded: bool = False):
        if not is_base64_encoded:
            self.document = document
        else:
            self._document = document

    @property
    def document(self) -> str:
        return decode_base64(self._document)

    @document.setter
    def document(self, document: Optional[str]):
        if document is not None:
            self._document = encode_base64(document)

    @property
    def document_b64(self) -> str:
        return self._document

    @document_b64.setter
    def document_b64(self, document: str):
        self._document = document


class TransformDocumentRequest(BaseModel, B64DocumentField):
    def __init__(
        self,
        document: str,
        service_name: str,
        file_name: Optional[str] = None,
        options: Optional[Options] = None,
        is_base64_encoded: bool = False,
    ) -> None:
        super().__init__(document=document, is_base64_encoded=is_base64_encoded)
        self.service_name = service_name
        self.file_name = file_name
        self.options = options

    def as_dict(self) -> RawTransformDocumentRequest:
        """Creates a dict of the object instance.

        Returns:
            RawTransformDocumentResponse: TransformDocumentResponse as dict.
        """
        return RawTransformDocumentRequest(
            document=self.document_b64,
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
        is_base64_encoded: bool = False,
    ) -> None:
        super().__init__(document=document, is_base64_encoded=is_base64_encoded)
        self.output = output
        self.error = error

    def as_dict(self) -> RawTransformDocumentResponse:
        """Creates a dict of the object instance.

        Returns:
            RawTransformDocumentResponse: TransformDocumentResponse as dict.
        """
        return RawTransformDocumentResponse(
            document=self.document_b64, output=self.output, error=self.error,
        )


@dataclass
class ServiceInfo(BaseModel):
    name: str

    def as_dict(self) -> RawServiceInfo:
        """Creates a dict of the object instance.

        Returns:
            RawServiceInfo: ServiceInfo as dict.
        """
        return RawServiceInfo(name=self.name,)


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


class PipeService(BaseModel):
    name: str
    options: Options

    def as_dict(self) -> RawPipeService:
        return RawPipeService(name=self.name, options=self.options.as_dict())


# TODO: implement base64 encode decode
class TransformDocumentPipeRequest(BaseModel, B64DocumentField):
    def __init__(
        self,
        document: str,
        services: List[ServiceInfo],
        file_name: Optional[str] = None,
        is_base64_encoded: bool = False,
    ) -> None:
        super().__init__(document=document, is_base64_encoded=is_base64_encoded)

        self.services = services
        self.file_name = file_name

    def as_dict(self) -> RawTransformDocumentPipeRequest:
        return RawTransformDocumentPipeRequest(
            document=self.document_b64,
            file_name=self.file_name,
            services=[info.as_dict() for info in self.services],
        )


class TransformDocumentPipeResponse(TransformDocumentResponse, B64DocumentField):
    def __init__(
        self,
        document: str,
        last_transformer: str,
        is_base64_encoded: bool = False,
        output: Optional[List[str]] = None,
        error: Optional[List[str]] = None,
    ):
        super().__init__(
            document=document,
            output=output,
            error=error,
            is_base64_encoded=is_base64_encoded,
        )
        self.last_transformer = last_transformer

    def as_dict(self) -> RawTransformDocumentPipeResponse:
        return RawTransformDocumentPipeResponse(
            document=self.document_b64,
            last_transformer=self.last_transformer,
            output=self.output,
            error=self.error,
        )


class OptionsPropertyError(BaseModel):
    name: str
    message: str

    def as_dict(self) -> RawOptionsPropertyError:
        return RawOptionsPropertyError(name=self.name, message=self.message)


class OptionsErrorResponse(BaseModel):
    code: int
    properties: List[OptionsPropertyError]

    def as_dict(self) -> RawOptionsErrorResponse:
        return RawOptionsErrorResponse(
            code=self.code,
            properties=[property.as_dict() for property in self.properties],
        )


class ErrorResponse(BaseModel):
    code: int
    message: str

    def as_dict(self) -> RawErrorResponse:
        return RawErrorResponse(code=self.code, message=self.message)

