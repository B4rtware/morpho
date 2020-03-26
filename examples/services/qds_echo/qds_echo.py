from pathlib import Path
import sys
from typing import Optional, Tuple
from grpc import ServicerContext

sys.path.append(str(Path(".").resolve()))

from service.proto.dtaservice_pb2 import DocumentRequest
from service.server import DTAServer


class QDS_ECHO(DTAServer):
    version = "0.0.1"
    app_name = "DE.TU-BERLIN.QDS.ECHO"

    def work(
        self, request: DocumentRequest, context: ServicerContext
    ) -> Tuple[str, Optional[str]]:
        return

    # def work(self, request, context) -> Tuple[str, Optional[str]]:
    #     return (request.document.decode(), None)


QDS_ECHO.run()
