from enum import Enum

# from morpho.rest.models import ServiceInfo
from typing import Callable, Dict, NewType, Optional
from pydantic import BaseModel

# if TYPE_CHECKING:
# # FIXME: change to type checking import and wait for issue answer
# from morpho.config import BaseConfig

# fmt: off
Worker = Callable[[str, Optional[BaseModel]], str]
# fmt: on

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
Headers = NewType("Headers", Dict[str, str])
