import dataclasses
from dataclasses import dataclass
import json
import logging as log
from pathlib import Path
from typing import Union

log.basicConfig(level=log.INFO)

# TODO:: consider to move the parser logic into this module e.g init() / parse()

# doctrans: DocTransServer
@dataclass
class DTAServerConfig:
    """Configuration class for a DTA server.

    It is a direct mapping for a given configuration file. Which should only contain
    options which are also supported by this class.
    """

    register: bool = False
    registrar_url: str = "http://localhost:8761/eureka"
    registrar_user: str = ""
    ttl: int = 0

    host_name: str = ""
    app_name: str = ""
    port_to_listen: str = "50000"
    dta_type: str = ""
    is_ssl: bool = False
    rest: bool = False
    http_port: str = "8080"

    log_level: str = ""
    config_file: str = "./dts/config.json"
    init: bool = False

    # doctrans: new_config_file
    def save(self) -> None:
        """Save the DTA configuration to the path specified in the DTA configuration.
        """
        path = Path(self.config_file)
        path.parent.mkdir(exist_ok=True, parents=True)
        with path.open("w") as configuration:
            json.dump(dataclasses.asdict(self), configuration, indent=4)

    # doctrans: new_doc_trans_from_file
    @classmethod
    def load(cls, path: Union[Path, str]) -> "DTAServerConfig":
        """Load a DTA configuration file from a given path.

        Returns:
            DTAServerConfig -- A new DTAServerConfig with provided options.
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
