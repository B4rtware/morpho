from pathlib import Path
import dataclasses
from dataclasses import dataclass
import socket
import logging as log
import json

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

    def setup_proxy_connection(self):
        print("hook up proxy connection")

    # doctrans: new_config_file
    def save(self):
        path = Path(self.CfgFile)
        path.parent.mkdir(exist_ok=True, parents=True)
        with path.open("w") as cfg:
            json.dump(dataclasses.asdict(self), cfg, indent=4)
        log.info("Wrote example configuration file to {}. Exiting".format(self.CfgFile))
        exit(0)
        return

    # TODO: implement here grpc and rest server?

    # doctrans: new_doc_trans_from_file
    @classmethod
    def load(cls, path) -> "DTAServerConfig":
        dtas_config = cls()
        with Path(path).open("r") as file:
            config = json.load(file)
            for arg in config.items():
                if arg[1]:
                    setattr(dtas_config, arg[0], arg[1])
        return dtas_config
