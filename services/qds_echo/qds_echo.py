from pathlib import Path
import sys
from typing import Optional, Tuple

sys.path.append(str(Path(".").resolve()))

from dtaservice.server import DTAServer

class QDS_ECHO(DTAServer):
    version = "0.0.1"
    app_name = "DE.TU-BERLIN.QDS.ECHO"

    def work(self, request, context) -> Tuple[str, Optional[str]]:
        return (request.document.decode(), None)

QDS_ECHO.run()