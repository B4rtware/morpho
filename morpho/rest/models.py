from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from morpho.types import ServiceStatus


# its models raw responses

# TODO: remove boilerplate code
# TODO: consider to create a warning if the document is empty

# TODO: consider to use a normal class here insteat of dataclasses because of the weird issure with intellisense
# TODO: consider to use a dataclasses if the problem is solved with having a dataclass and properties


# def __init__(self, **data) -> None:
#     try:
#         super().__init__(**data)
#     except ValidationError as e:
#         errors = []
#         for prop in json.loads(e.json()):
#             errors.append(
#                 OptionsPropertyError(
#                     name=",".join(prop["loc"]),
#                     message="{}: {}".format(prop["type"], prop["msg"]),
#                 )
#             )
#         options_error_response = OptionsErrorResponse(code=504, properties=errors)
#         raise ServerOptionsValidationError(error=options_error_response)


class Model(BaseModel):
    class Config:
        extra = "forbid"


class Health(BaseModel):
    status: ServiceStatus = ServiceStatus.UP


class ServiceInfo(Model):
    name: str
    options: Optional[Dict[str, Any]]


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
    options: Optional[Dict[str, Any]] = None


class PipeService(Model):
    name: str
    options: Optional[Dict[str, Any]]


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
