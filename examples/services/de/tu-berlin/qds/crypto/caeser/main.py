from morpho.server import Service
from pydantic import BaseModel


class Options(BaseModel):
    offset: int = 0


def work(document: str, options: Options) -> str:
    document = document.capitalize()
    return "".join(
        [chr(((ord(char) - 65 + options.offset) % 26) + 65) for char in document]
    )


service = Service(name="caeser", version="0.0.1", options_type=Options, worker=work)

if __name__ == "__main__":
    service.run()
