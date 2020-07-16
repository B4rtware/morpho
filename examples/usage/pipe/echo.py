from morpho.config import BaseConfig
from typing import Optional
from morpho.server import Service


echo = Service(name="ECHO", version="1.0.1")


@echo.worker
def echo_worker(document: str, _: Optional[BaseConfig]) -> str:
    print("ECHO")
    return document


if __name__ == "__main__":
    echo.run(port=50001)
