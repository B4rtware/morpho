from typing import TYPE_CHECKING, List, Optional, Type

from pydantic import BaseModel
from pydantic import Field

from morpho.rest.models import Health
from morpho.types import DtaType

if TYPE_CHECKING:
    from morpho.consumer import WorkConsumer


class ServiceConfig(BaseModel):
    """Configuration class for a morpho server.

    It is a direct mapping for a given configuration file. Which should only contain
    options which are also supported by this class.
    """

    name: str = ""
    version: str = ""
    consumers: Optional[List[Type["WorkConsumer"]]] = None

    should_register: bool = Field(default=False, alias="register")
    registrar_url: str = "http://localhost:8761/eureka"
    registrar_user: str = ""
    ttl: int = 0

    host_name: str = ""
    port_to_listen: str = "50000"
    type: DtaType = DtaType.SERVICE
    is_ssl: bool = False
    rest: bool = False
    http_port: str = "8080"

    log_level: str = ""
    timeout: float = 20
    init: bool = False

    health: Health = Field(default_factory=Health)
