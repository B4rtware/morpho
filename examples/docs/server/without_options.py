""" A minimal working example which defines a simple service
    and a document transform function."""
from morpho.server import Service


def work(document: str) -> str:
    return document


service = Service(name="Echo", version="0.0.1", worker=work)

if __name__ == "__main__":
    service.run()
