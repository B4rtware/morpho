from pathlib import Path
from grpc import ServicerContext
from service.proto.dtaservice_pb2 import DocumentRequest
import sys
from typing import Optional, Tuple

sys.path.append(str(Path(".").resolve()))

from service.server import DTAServer


class QDS_COUNT_CHAR(DTAServer):
    version = "0.0.1"
    app_name = "QDS.ECHO"

    def work(
        self, request: DocumentRequest, context: ServicerContext
    ) -> Tuple[str, Optional[str]]:
        document = str(request.document)
        return (f"The document has {len(document)} characters.", None)


QDS_COUNT_CHAR.run()
