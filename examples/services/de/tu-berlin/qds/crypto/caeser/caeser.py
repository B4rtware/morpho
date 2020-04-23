
from dataclasses import dataclass
from service.config import BaseConfig
from service.server import DTAServer

@dataclass
class Options(BaseConfig):
    offset: int = 0

class Caeser(DTAServer):
    version = "0.0.1"
    name = "de.tu-berlin.qds.crypto.caeser"
    options = Options()

    def work(self, document: str, options: Options) -> str:
        document = document.capitalize()
        return "".join([chr(((ord(char) - 65 + options.offset) % 26) + 65) for char in document])