from morpho.config import BaseConfig
from typing import Optional
from morpho.consumer import RestWorkConsumer
from morpho.server import Service

service = Service(
    name="DE.TU-BERLIN.ECHO",
    version="1.0.0",
    protocols=[RestWorkConsumer]
)

@service.worker
def work(document: str, _: Optional[BaseConfig] = None) -> str:
    return document

if __name__ == "__main__":
    service.run(50001)