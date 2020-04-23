import dataclasses
from dataclasses import dataclass
import json
import logging as log
from pathlib import Path
from typing import Any, Dict, IO, Optional, Union

from morpho.types import ServiceType

log.basicConfig(level=log.INFO)

# TODO: consider to move the parser logic into this module e.g init() / parse()
# TODO: use loads load dump dumps


@dataclass
class BaseConfig:
    """Base Configuration class for a morpho server."""

    config_file: str = "./dts/config.json"

    def as_json(self, indent: Optional[int] = None) -> str:
        """[summary]
        
        Args:
            indent (Optional[int], optional): [description]. Defaults to None.
        
        Returns:
            str: [description]
        """
        return json.dumps(dataclasses.asdict(self), indent=indent)

    def as_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    # doctrans: new_config_file
    def save(self, file: Optional[IO]) -> None:
        """Save the morpho configuration to the path specified in the morpho configuration.
        
        If not provided it will saves the configuration file to the specified path in the
        configuration object.

        Args:
            file (Optional[IO]): A IO descriptor. Defaults to None.
        """
        if not file:
            path = Path(self.config_file)
            path.parent.mkdir(exist_ok=True, parents=True)
            with path.open("w") as configuration:
                json.dump(dataclasses.asdict(self), configuration, indent=4)
        else:
            out = json.dumps(dataclasses.asdict(self), indent=4)
            file.write(out)

    # doctrans: new_doc_trans_from_file
    @classmethod
    def load(cls, path: Union[Path, str]) -> "ServerConfig":
        """Load a morpho configuration file from a given path.

        Returns:
            ServerConfig -- A new ServerConfig with provided options.
        """
        if not isinstance(path, str):
            path = Path(path)
        dtas_config = cls()
        # open file and add each option to the created configuration instance
        with Path(path).open("r") as file:
            config = json.load(file)
            for arg in config.items():
                if arg[1]:
                    setattr(dtas_config, arg[0], arg[1])
        return dtas_config


# doctrans: DocTransServer
@dataclass
class ServerConfig(BaseConfig):
    """Configuration class for a morpho server.

    It is a direct mapping for a given configuration file. Which should only contain
    options which are also supported by this class.
    """

    app_name: str = ""
    version: str = ""
    options: Optional[BaseConfig] = None

    register: bool = False
    registrar_url: str = "http://localhost:8761/eureka"
    registrar_user: str = ""
    ttl: int = 0

    host_name: str = ""
    port_to_listen: str = "50000"
    service_type: ServiceType = ServiceType.SERVICE
    is_ssl: bool = False
    rest: bool = False
    http_port: str = "8080"

    log_level: str = ""
    init: bool = False