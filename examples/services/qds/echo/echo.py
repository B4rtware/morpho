from pathlib import Path
import sys

sys.path.append(str(Path(".").resolve()))

from service.server import DTAServer

class QDS_ECHO(DTAServer):
    version = "0.0.1"
    name = "DE.TU-BERLIN.QDS.ECHO"

    def work(self, document: str) -> str:
        return document


QDS_ECHO.run()
