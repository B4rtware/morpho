from dataclasses import dataclass
import dataclasses
from pathlib import Path
import sys
import json
from typing import Optional, Tuple

sys.path.append(str(Path(".").resolve()))

from dtaservice.server import DTAServer

@dataclass
class CountResults():
    Bytes: int
    Lines: int
    Words: int

class QDS_COUNT(DTAServer):
    version = "0.0.1"
    app_name = "QDS.ECHO"

    def work(self, input: str) -> Tuple[str, Optional[str]]:
        cr = CountResults(
            Bytes = len(input.encode()),
            Lines = len(input.split("\n")) - 1,
            Words = len(input.split("\n"))
        )
        return (json.dumps(dataclasses.asdict(cr)), None)

QDS_COUNT.run()