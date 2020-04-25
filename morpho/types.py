from enum import Enum
from typing import Any, Dict, List, NewType, Optional, TypedDict


# must resides here because otherwise circular import
class ServiceType(Enum):
    """Type for a Service"""

    SERVICE = "service"
    PROXY = "proxy"
    GATEWAY = "gateway"

# TODO consider to use dicttypes
Options = NewType("Options", Dict[str, Any])
Headers = NewType("Headers", Dict[str, str])


# +-------------------------------------------------------------------------------------+
# |                                  Raw Dict Types                                     |
# +-------------------------------------------------------------------------------------+


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


class RawListService(TypedDict):
    """Raw ListService dict type"""

    name: str
    version: str
    options: Dict[str, Any]


class RawServiceInfo(TypedDict):
    """Raw ServiceInfo dict type"""

    name: str
    version: str
    options: Optional[Dict[str, Any]]


class RawListResponse(TypedDict):
    """Raw ListResponse dict type"""

    services: List[RawListService]


class RawTransformDocumentPipeRequest(RawTransformDocumentRequest):
    """Raw TransformDocumentPipeRequest dict type"""

    services: List[Dict[str, Any]]


class RawTransformDocumentPipeResponse(RawTransformDocumentResponse):
    """Raw TransformDocumentPipeResponse dict type"""

    sender: str
