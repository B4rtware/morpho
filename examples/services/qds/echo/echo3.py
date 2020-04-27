from dataclasses import dataclass
from pathlib import Path

import sys
from pathlib import Path
sys.path.append(str(Path(".").resolve()))
from morpho.config import BaseConfig
import sys

sys.path.append(str(Path(".").resolve()))

from morpho.server import Server, run_app

@dataclass
class Options(BaseConfig):
    offset: int = 5

@run_app(port=50005)
class Echo(Server):
    """Simple echo server which will return the 
    """
    # TODO: expose this in list services
    # TODO: create metadata field for options and version
    version = "0.0.1"
    name = "DE.TU-BERLIN.QDS.ECHOS3"
    # TODO: implement build in consumer
    # options = Options()

    def work(self, document: str, options: Options) -> str:
        print(self.config.app_name)
        return document + "ECHO3"
