from threading import Thread
import requests as r

from pathlib import Path
import sys
sys.path.append(str(Path(".").resolve()))
from service.server import DTAServer

class QDS_TEST(DTAServer):
    version = "0.0.1"
    name = "TEST"
    def work(self, document: str) -> str:
        return document
         

def test_integration_rest():
    # TODO: use a client to interact with the server to use more than one component?
    # remove all other program arguments and add the rest protocol
    sys.argv = [sys.argv[0], "--Protocols=rest"]

    # app = QDS_TEST
    app_thread = Thread(target=QDS_TEST.run, daemon=True)
    app_thread.start()

    app_thread.join(timeout=1)
    assert app_thread.is_alive()

    result = r.post("http://127.0.0.1:8080/v1/qds/dta/document/transform", json={ "document": "Hello World!" })
    document_response = result.json()
    assert document_response["trans_document"] == "Hello World!"
    # print(result)

