
from dataclasses import dataclass
from typing import List
from service.config import BaseConfig
from service.server import DTAServer

@dataclass
class Options(BaseConfig):
    pi: List[int] = [2,4,1,2]

class Permutation(DTAServer):
    version = "0.0.1"
    name = "de.tu-berlin.qds.crypto.permutation"
    options = Options()

    def work(self, document: str, options: Options) -> str:
        stack = list(document)

        index = 0
        while (index + len(options.pi)) < len(stack):
            section = stack[index:index+len(options.pi)]
            for i, char in zip(options.pi, section):
                stack[index + i] = char
            index += len(options.pi)

        return "".join(stack)