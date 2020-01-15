from pathlib import Path
import dataclasses
from dataclasses import dataclass
import dtaservice.dtaservice_pb2 as dtaservice_pb2
import socket
import logging as log
import json

log.basicConfig(level=log.INFO)

APP_NAME = "DE.TU-BERLIN.QDS.ABSTRACT-SERVER"

@dataclass
class DocTransServer:
    RegistrarURL: str = ""
    RegistrarUser: str = ""
    TTL: int = 0

    HostName: str = ""
    AppName: str = ""
    PortToListen: str = ""
    DtaType: str = ""
    IsSSL: bool = False

    LogLevel: int = 0
    CfgFile: str = "./dts/config.json"
    Init: bool = False

    def new_config_file(self):
        path = Path(self.CfgFile)
        path.parent.mkdir(exist_ok=True, parents=True)
        with path.open("w") as cfg:
            json.dump(dataclasses.asdict(self), cfg, indent=4)
        log.info("Wrote example configuration file to {}. Exiting".format(self.CfgFile))
        exit(0)
        return

    def create_listener(self, max_port_seeks):
        port = int(self.PortToListen)
        log.debug("sajidj")
        print("hello")
        for i in range(max_port_seeks):
            log.info("Trying to listen on port {}".format(port))
            address = ("", port)
            s = socket.create_server(address)
            if s:
                log.info("Using port {} to listen for dta".format(port))
                break
            else:
                log.error("Error while creating socket!")
                exit(1)

        s.listen(1)
        conn, addr = s.accept()

    @classmethod
    def new_doc_trans_from_file(cls, path):
        with Path(self.CfgFile).open("r") as file:
            json.load(file)

