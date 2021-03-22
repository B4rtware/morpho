from morpho.server import Service
from pydantic import BaseModel


class Options(BaseModel):
    name: str


def work(document: str, options: Options) -> str:
    return document + options.name


service = Service(name="AppendName", version="0.0.1", worker=work, options_type=Options)

if __name__ == "__main__":
    service.run()
