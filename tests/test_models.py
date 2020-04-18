from service.server import Options, RawTransformDocumentPipeRequest, RawTransformDocumentRequest, RawTransformDocumentPipeResponse
from service.rest.models import ListServicesResponse, TransformDocumentPipeRequest, TransformDocumentPipeResponse, TransformDocumentRequest, TransformDocumentResponse
from base64 import b64encode
import pytest
import binascii
import json


class TestTransformDocumentRequest():

    B64_HELLO_WORLD = b64encode("Hello World!".encode("utf-8")).decode("utf-8")

    def test_document_validation_success(self):
        request = TransformDocumentRequest(document=self.B64_HELLO_WORLD, service_name="")
        assert request.document == self.B64_HELLO_WORLD

    def test_document_validation_failure(self):
        with pytest.raises(binascii.Error, match="Please make sure your document string is base64 encoded!"):
            TransformDocumentRequest(document="Hello World!", service_name="")

    def test_asdict_required_params(self):
        request = TransformDocumentRequest(document=self.B64_HELLO_WORLD, service_name="QDS.TEST")
        request_dict = request.as_dict()
        assert len(request_dict.keys()) == 4
        assert request_dict["document"] == self.B64_HELLO_WORLD
        assert request_dict["service_name"] == "QDS.TEST"
        assert request_dict["file_name"] is None
        assert request_dict["options"] is None

    def test_asdict_all_params(self):
        # TODO: pyright issue?
        options: Options = {"offset": 8}
        request = TransformDocumentRequest(document=self.B64_HELLO_WORLD, service_name="QDS.TEST", file_name="file.txt", options=options)
        request_dict = request.as_dict()
        assert len(request_dict.keys()) == 4
        assert request_dict["document"] == self.B64_HELLO_WORLD
        assert request_dict["service_name"] == "QDS.TEST"
        assert request_dict["file_name"] == "file.txt"
        assert request_dict["options"] == options

    def test_asjson_required_params(self):
        request = TransformDocumentRequest(document=self.B64_HELLO_WORLD, service_name="QDS.TEST")
        assert request.as_json() == '{"document": "SGVsbG8gV29ybGQh", "service_name": "QDS.TEST", "file_name": null, "options": null}'

    def test_asjson_all_params(self):
        request = TransformDocumentRequest(document=self.B64_HELLO_WORLD, service_name="QDS.TEST", file_name="file.txt", options={"offset": 4})
        assert request.as_json() == '{"document": "SGVsbG8gV29ybGQh", "service_name": "QDS.TEST", "file_name": "file.txt", "options": {"offset": 4}}'

class TestTransformDocumentResponse():

    B64_HELLO_WORLD_BACK = b64encode("Hello World Back!".encode("utf-8")).decode("utf-8")

    def test_trans_document_validation_success(self):
        response = TransformDocumentResponse(trans_document=self.B64_HELLO_WORLD_BACK)
        assert response.trans_document == self.B64_HELLO_WORLD_BACK

    def test_trans_document_validation_failure(self):
        with pytest.raises(binascii.Error, match="Please make sure your document string is base64 encoded!"):
            TransformDocumentResponse(trans_document="Hello World Back!")

    def test_asdict_required_params(self):
        response = TransformDocumentResponse(trans_document=self.B64_HELLO_WORLD_BACK)
        response_dict = response.as_dict()
        assert len(response_dict.keys()) == 3
        assert response_dict["trans_document"] == self.B64_HELLO_WORLD_BACK
        assert response_dict["trans_output"] is None
        assert response_dict["error"] is None

    def test_asdict_all_params(self):
        response = TransformDocumentResponse(trans_document=self.B64_HELLO_WORLD_BACK, trans_output=["OUTPUT 1", "OUTPUT 2"], error=["ERROR 1", "ERROR 2"])
        response_dict = response.as_dict()
        assert len(response_dict.keys()) == 3
        assert response_dict["trans_document"] == self.B64_HELLO_WORLD_BACK
        assert response_dict["trans_output"] == ["OUTPUT 1", "OUTPUT 2"]
        assert response_dict["error"] == ["ERROR 1", "ERROR 2"]

    def test_asjson_required_params(self):
        response = TransformDocumentResponse(trans_document=self.B64_HELLO_WORLD_BACK)
        assert response.as_json() == '{"trans_document": "SGVsbG8gV29ybGQgQmFjayE=", "trans_output": null, "error": null}'

    def test_asjson_all_params(self):
        response = TransformDocumentResponse(trans_document=self.B64_HELLO_WORLD_BACK, trans_output=["OUTPUT 1", "OUTPUT 2"], error=["ERROR 1", "ERROR 2"])
        assert response.as_json() == '{"trans_document": "SGVsbG8gV29ybGQgQmFjayE=", "trans_output": ["OUTPUT 1", "OUTPUT 2"], "error": ["ERROR 1", "ERROR 2"]}'

class TestListServicesResponse():

    def test_asdict(self):
        response = ListServicesResponse(services=["QDS.TEST", "QDS.ECHO"])
        response_dict = response.as_dict()
        assert len(response_dict.keys()) == 1
        assert response_dict["services"] == ["QDS.TEST", "QDS.ECHO"]

    def test_asjson(self):
        response = ListServicesResponse(services=["QDS.TEST", "QDS.ECHO"])
        assert response.as_json() == '{"services": [{"name": "QDS.TEST", "options": {""}, "QDS.ECHO"]}'

class TestTransformDocumentPipeRequest():
    B64_HELLO_WORLD_PIPE = b64encode("Hello World Pipe!".encode("utf-8")).decode("utf-8")

    def test_trans_document_validation_success(self):
        request = TransformDocumentPipeRequest(document=self.B64_HELLO_WORLD_PIPE, service_name="", services=[{}])
        assert request.document == self.B64_HELLO_WORLD_PIPE

    def test_trans_document_validation_failure(self):
        with pytest.raises(binascii.Error, match="Please make sure your document string is base64 encoded!"):
            TransformDocumentPipeRequest(document="Hello World Pipe!", service_name="", services=[{}])

    def test_asdict_required_params(self):
        request = TransformDocumentPipeRequest(document=self.B64_HELLO_WORLD_PIPE, service_name="QDS.TEST", services=[
            {
                "name": "QDS.ECHO",
                "options": {
                    "offset": 5
                }
            }
        ])
        request_dict = request.as_dict()
        assert request_dict["document"] == self.B64_HELLO_WORLD_PIPE
        assert request_dict["service_name"] == "QDS.TEST"
        assert request_dict["services"] == [{"name": "QDS.ECHO", "options": { "offset": 5 }}]
        assert request_dict["file_name"] is None
        assert request_dict["options"] is None

    def test_asdict_all_params(self):
        request = TransformDocumentPipeRequest(document=self.B64_HELLO_WORLD_PIPE, service_name="QDS.TESTO", services=[
            {
                "name": "QDS.COUNT",
                "options": {
                    "debug": True
                }
            }
        ], file_name="secret.txt", options={"offset": 7})
        request_dict = request.as_dict()
        assert request_dict["document"] == self.B64_HELLO_WORLD_PIPE
        assert request_dict["service_name"] == "QDS.TESTO"
        assert request_dict["services"] == [{"name": "QDS.COUNT", "options": { "debug": True }}]
        assert request_dict["file_name"] == "secret.txt"
        assert request_dict["options"] == {"offset": 7}

    def test_asjson_required_params(self):
        request = TransformDocumentPipeRequest(document=self.B64_HELLO_WORLD_PIPE, service_name="QDS.CEASER", services=[
            {
                "name": "QDS.COUNT",
                "options": {
                    "validate": True
                }
            }
        ])
        assert request.as_json() == '{"document": "SGVsbG8gV29ybGQgUGlwZSE=", "service_name": "QDS.CEASER", "file_name": null, "options": null, "services": [{"name": "QDS.COUNT", "options": {"validate": true}}]}'

    def test_asjson_all_params(self):
        request = TransformDocumentPipeRequest(document=self.B64_HELLO_WORLD_PIPE, service_name="QDS.EMAIL", services=[
            {
                "name": "QDS.EMPTY",
                "options": {
                    "line": {
                        "limit": 10
                    }
                }
            }
        ], file_name="sec.txt", options={"debug": True})
        assert request.as_json() == '{"document": "SGVsbG8gV29ybGQgUGlwZSE=", "service_name": "QDS.EMAIL", "file_name": "sec.txt", "options": {"debug": true}, "services": [{"name": "QDS.EMPTY", "options": {"line": {"limit": 10}}}]}'

class TestTransformDocumentPipeResponse():
    B64_HELLO_WORLD_PIPE_BACK = b64encode("Hello World Pipe Back!".encode("utf-8")).decode("utf-8")

    def test_trans_document_validation_success(self):
        response = TransformDocumentPipeResponse(trans_document=self.B64_HELLO_WORLD_PIPE_BACK, sender="QDS.TST")
        print(vars(response))
        assert response.trans_output == self.B64_HELLO_WORLD_PIPE_BACK