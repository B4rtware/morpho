from typing import List, Optional, TypedDict

from pydantic.main import BaseModel


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
    options: Optional[BaseModel]


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
    options: BaseModel


class RawOptionsPropertyError(TypedDict):
    name: str
    message: str


class RawOptionsErrorResponse(TypedDict):
    code: int
    properties: List[RawOptionsPropertyError]


class RawErrorResponse(TypedDict):
    code: int
    message: str
