from pathlib import Path
import sys
from typing import Optional, Tuple, Union

sys.path.append(str(Path(".").resolve()))

from services.services import DTAServer

class QDS_COUNT_CHAR(DTAServer):
    version = "0.0.1"
    app_name = "QDS.ECHO"

    def work(self, input: str) -> Tuple[str, Optional[str]]:
        return (f"The document has {len(input)} characters.", None)

QDS_COUNT_CHAR.run()