from pydantic.main import BaseModel
from morpho.server import Service


def work(document: str, _: BaseModel):
    return document


service = Service(name="ECHO", version="0.1.0", worker=work)

if __name__ == "__main__":
    service.run(50000)
