from dataclasses import dataclass
from pydantic import BaseModel
from morpho.util import decode_base64, encode_base64

# from morpho.config import BaseConfig
from typing import List, Optional


# its models raw responses

# TODO: remove boilerplate code
# TODO: consider to create a warning if the document is empty

# TODO: consider to use a normal class here insteat of dataclasses because of the weird issure with intellisense
# TODO: consider to use a dataclasses if the problem is solved with having a dataclass and properties


class Model(BaseModel):
    class Config:
        extra = "forbid"


class ServiceInfo(Model):
    name: str


class ListServicesResponse(Model):
    services: List[ServiceInfo]


class TransformDocumentResponse(Model):
    document: str
    output: Optional[List[str]] = None
    error: Optional[List[str]] = None


class TransformDocumentRequest(Model):
    document: str
    service_name: str
    file_name: Optional[str] = None
    options: Optional[BaseModel] = None


class PipeService(Model):
    name: str
    options: Optional[BaseModel]


class TransformDocumentPipeRequest(Model):
    document: str
    services: List[PipeService]
    file_name: Optional[str] = None


class TransformDocumentPipeResponse(Model):
    document: str
    output: Optional[List[str]] = None
    error: Optional[List[str]] = None
    last_transformer: str


class OptionsPropertyError(Model):
    name: str
    message: str


class OptionsErrorResponse(Model):
    code: int
    properties: List[OptionsPropertyError]


class ErrorResponse(Model):
    code: int
    message: str
