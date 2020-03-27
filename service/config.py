import dataclasses
from dataclasses import dataclass
import json
import logging as log
from pathlib import Path
from typing import Union

log.basicConfig(level=log.INFO)

# doctrans: DocTransServer
@dataclass
class DTAServerConfig:
    RegistrarURL: str = "http://localhost:8761/eureka"
    RegistrarUser: str = ""
    TTL: int = 0

    HostName: str = ""
    AppName: str = ""
    PortToListen: str = "50000"
    DtaType: str = ""
    IsSSL: bool = False
    REST: bool = False
    HTTPPort: str = "8080"

    LogLevel: str = ""
    CfgFile: str = "./dts/config.json"
    Init: bool = False

    def setup_proxy_connection(self) -> None:
        print("hook up proxy connection")

    # doctrans: new_config_file
    def save(self) -> None:
        path = Path(self.CfgFile)
        path.parent.mkdir(exist_ok=True, parents=True)
        with path.open("w") as f:
            json.dump(dataclasses.asdict(self), f, indent=4)

    # TODO: implement here grpc and rest server?

    # doctrans: new_doc_trans_from_file
    @classmethod
    def load(cls, path: Union[Path, str]) -> "DTAServerConfig":
        if not isinstance(path, str):
            path = Path(path)
        dtas_config = cls()
        with Path(path).open("r") as file:
            config = json.load(file)
            for arg in config.items():
                if arg[1]:
                    setattr(dtas_config, arg[0], arg[1])
        return dtas_config
