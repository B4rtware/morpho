from pydantic import BaseModel
from morpho.server import Service

# TODO: option to add info about option


class Options(BaseModel):
    key: str = "LEMON"


service = Service(
    name="vigenere", version="0.0.1", options_type=Options
)


@service.worker
def work(document: str, options: Options) -> str:
    document = document.capitalize()
    key = options.key.capitalize()
    encrypted = ""
    for index, char in enumerate(document):
        key_char = key[index % len(key)]
        encrypted += chr((((ord(char) - 65) + (ord(key_char) - 65)) % 26) + 65)
    return encrypted


if __name__ == "__main__":
    service.run()

