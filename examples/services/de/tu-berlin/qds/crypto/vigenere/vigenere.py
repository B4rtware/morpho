
from dataclasses import dataclass
from service.config import BaseConfig
from service.server import DTAServer

# TODO: option to add info about option

@dataclass
class Options(BaseConfig):
    key: str = "LEMON"

class Permutation(DTAServer):
    version = "0.0.1"
    name = "de.tu-berlin.qds.crypto.vigenere"
    options = Options()

    def work(self, document: str, options: Options) -> str:
        document = document.capitalize()
        key = options.key.capitalize()
        encrypted = ""
        for index, char in enumerate(document):
            key_char = key[index % len(key)]
            encrypted += chr((((ord(char) - 65) + (ord(key_char) - 65)) % 26)+65)
        return encrypted