from morpho.server import Service
from typing import Optional
from morpho.config import BaseConfig


lower = Service(name="LOWER", version="1.2.3")


@lower.worker
def lower_worker(document: str, _: Optional[BaseConfig]) -> str:
    print("LOWER")
    return document.lower()


if __name__ == "__main__":
    lower.run(port=50000)
