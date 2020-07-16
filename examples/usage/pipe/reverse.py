from typing import Optional
from morpho.server import Service
from morpho.config import BaseConfig


reverse = Service(name="REVERSE", version="1.0.2")


@reverse.worker
def reverse_worker(document: str, _: Optional[BaseConfig]) -> str:
    print("REVERSE")
    return "".join(list(reversed(document)))


if __name__ == "__main__":
    reverse.run(port=50002)
