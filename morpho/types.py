from enum import Enum
# from morpho.rest.models import ServiceInfo
from typing import Any, Dict, List, NewType, Optional, TypedDict


# must resides here because otherwise circular import
class ServiceType(Enum):
    """Type for a Service"""

    SERVICE = "service"
    PROXY = "proxy"
    GATEWAY = "gateway"

# @dataclass
# class Metadata(ServiceInfo):
#     def 

# TODO consider to use dicttypes
Options = NewType("Options", Dict[str, Any])
Headers = NewType("Headers", Dict[str, str])
