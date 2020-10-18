from enum import Enum

# from morpho.rest.models import ServiceInfo
from typing import Any, Callable, Dict, NewType, Union
from pydantic import BaseModel

# if TYPE_CHECKING:
# # FIXME: change to type checking import and wait for issue answer
# from morpho.config import BaseConfig

# fmt: off
Worker = Union[Callable[[str], str], Callable[[str, BaseModel], str]]
Schema = Dict[str, Any]
# fmt: on

# must resides here because otherwise circular import
class DtaType(str, Enum):
    """Document Transformation Application Type of a Service"""

    SERVICE = "service"
    GATEWAY = "gateway"
    UNKNOWN = "unknown"


class ServiceStatus(Enum):
    UP = "UP"
    DOWN = "DOWN"
    STARTING = "STARTING"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    UNKNOWN = "UNKNOWN"


# TODO consider to use dicttypes
Headers = NewType("Headers", Dict[str, str])
