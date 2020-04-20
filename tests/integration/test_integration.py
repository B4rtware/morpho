from threading import Thread
import requests as r

from pathlib import Path
import sys
sys.path.append(str(Path(".").resolve()))
from service.server import DTARestWorkConsumer, DTAServer

class QDS_TEST(DTAServer):
    version = "0.0.1"
    name = "TEST"
    consumer = ["rest"]

    def __init__(self) -> None:
        super().__init__()
        self.register_consumer("rest", DTARestWorkConsumer)

    def work(self, document: str) -> str:
        return document
         
# TODO: optimize by using a config and retry if ping fails
def test_integration_rest():
    # TODO: use a client to interact with the server to use more than one component?
    # remove all other program arguments and add the rest protocol
    sys.argv = [sys.argv[0], "--protocols=rest"]

    # app = QDS_TEST
    app_thread = Thread(target=QDS_TEST.run)
    app_thread.start()

    app_thread.join(timeout=10)
    assert app_thread.is_alive()

    result = r.post("http://127.0.0.1:50000/v1/qds/dta/document/transform", json={ "document": "Hello World!" })
    assert result.status_code == 200
    assert result.text
    document_response = result.json()
    assert document_response["trans_document"] == "Hello World!"

