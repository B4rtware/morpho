
from typing import List
from pydantic import BaseModel
from morpho.server import Service

class Options(BaseModel):
    pi: List[int] = [2,4,1,2]

service = Service(name="de.tu-berlin.qds.crypto.permutation", version="0.0.1", options=Options)

@service.worker
def work(document: str, options: Options) -> str:
    stack = list(document)

    index = 0
    while (index + len(options.pi)) < len(stack):
        section = stack[index:index+len(options.pi)]
        for i, char in zip(options.pi, section):
            stack[index + i] = char
        index += len(options.pi)

    return "".join(stack)

if __name__ == "__main__":
    service.run()

