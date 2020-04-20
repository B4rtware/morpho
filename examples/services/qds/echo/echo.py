from pathlib import Path
import sys

sys.path.append(str(Path(".").resolve()))

from service.server import DTAServer, run_app, DTARestWorkConsumer


@run_app
class QDS_ECHO(DTAServer):
    # TODO: expose this in list services
    # TODO: create metadata field for options and version
    version = "0.0.1"
    name = "DE.TU-BERLIN.QDS.ECHO"
    # TODO: implement build in consumer
    consumer = ["rest"]
    options = {
        "offset": 8
    }

    def __init__(self) -> None:
        super().__init__()
        self.register_consumer("newcosumer", DTARestWorkConsumer)

    def work(self, document: str) -> str:
        return document
