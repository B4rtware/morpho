from dataclasses import dataclass
import dataclasses
import json
from pathlib import Path
import sys
from typing import Optional, Tuple

from grpc import ServicerContext

sys.path.append(str(Path(".").resolve()))

from service.proto.dtaservice_pb2 import DocumentRequest
from service.server import DTAServer


@dataclass
class CountResults:
    Bytes: int
    Lines: int
    Words: int


class QDS_COUNT(DTAServer):
    version = "0.0.1"
    app_name = "QDS.ECHO"

    def work(
        self, request: DocumentRequest, context: ServicerContext
    ) -> Tuple[str, Optional[str]]:
        document = request.document
        cr = CountResults(
            Bytes=len(document),
            Lines=len(str(document).split("\n")) - 1,
            Words=len(str(document).split("\n")),
        )
        return (json.dumps(dataclasses.asdict(cr)), None)


QDS_COUNT.run()
