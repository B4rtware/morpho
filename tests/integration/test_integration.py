from base64 import b64encode
from base64 import b64decode
import sys
from threading import Thread

import requests as r

from morpho.server import RestWorkConsumer, Server

# TODO: create fixture for rest server
# TODO: rename to test_rest.py

class QDS_TEST(Server):
    version = "0.0.1"
    name = "TEST"
    consumer = ["rest"]

    def __init__(self) -> None:
        super().__init__()
        self.register_consumer("rest", RestWorkConsumer)

    def work(self, document: str) -> str:
        return document


# TODO: optimize by using a config and retry if ping fails
def test_rest_transform():
    # TODO: use a client to interact with the server to use more than one component?
    # remove all other program arguments and add the rest protocol
    sys.argv = [sys.argv[0], "--protocols=rest"]

    # app = QDS_TEST
    app_thread = Thread(target=QDS_TEST.run, daemon=True)
    app_thread.start()

    app_thread.join(timeout=5)
    assert app_thread.is_alive()

    result = r.post(
        "http://127.0.0.1:50000/v1/qds/dta/document/transform",
        json={"document": "Hello World!"},
    )
    assert result.status_code == 200
    assert result.text
    document_response = result.json()
    assert document_response["trans_document"] == "Hello World!"


def test_rest_list():
    sys.argv = [sys.argv[0], "--protocols=rest"]

    app_thread = Thread(target=QDS_TEST.run, daemon=True)
    app_thread.start()

    app_thread.join(timeout=5)
    assert app_thread.is_alive()
    result = r.get("http://127.0.0.1:50000/v1/qds/dta/service/list")
    assert result.status_code == 200
    assert result.text
    document_response = result.json()
    assert document_response["services"] == [
        {"name": "TEST", "options": None, "version": "0.0.1"}
    ]


# def test_rest_transform_pip():
#     sys.argv = [sys.argv[0], "--protocols=rest"]

#     app_thread = Thread(target=QDS_TEST.run, daemon=True)
#     app_thread.start()

#     app_thread.join(timeout=5)
#     assert app_thread.is_alive()

#     data = {"document": b64encode("Hello I want to be piped.")}
