from pydantic.main import BaseModel
from morpho.rest.models import (
    ListServicesResponse,
    ServiceInfo,
    TransformDocumentPipeRequest,
    TransformDocumentPipeResponse,
    TransformDocumentRequest,
    TransformDocumentResponse,
)
from morpho.util import decode_base64, encode_base64


class TestTransformDocumentRequest:
    class TempOptions(BaseModel):
        offset: int

    def test_asdict_required_params(self):
        request = TransformDocumentRequest(
            document=encode_base64("Hello World!"), service_name="QDS.TEST"
        )
        request_dict = request.dict()
        assert len(request_dict.keys()) == 4
        assert request_dict["document"] == "SGVsbG8gV29ybGQh"
        assert request_dict["service_name"] == "QDS.TEST"
        assert request_dict["file_name"] is None
        assert request_dict["options"] is None

    def test_asdict_all_params(self):
        # TODO: pyright issue?
        options = self.TempOptions(offset=8)
        request = TransformDocumentRequest(
            document=encode_base64("Hello World2!"),
            service_name="QDS.TEST",
            file_name="file.txt",
            options=options,
        )
        request_dict = request.dict()
        assert len(request_dict.keys()) == 4
        assert request_dict["document"] == "SGVsbG8gV29ybGQyIQ=="
        assert request_dict["service_name"] == "QDS.TEST"
        assert request_dict["file_name"] == "file.txt"
        assert request_dict["options"] == options.dict()

    def test_asjson_required_params(self):
        request = TransformDocumentRequest(
            document=encode_base64("Hello World3!"), service_name="QDS.TEST"
        )
        assert (
            request.json()
            == '{"document": "SGVsbG8gV29ybGQzIQ==", "service_name": "QDS.TEST", "file_name": null, "options": null}'
        )

    def test_asjson_all_params(self):
        request = TransformDocumentRequest(
            document=encode_base64("Hello World4!"),
            service_name="QDS.TEST",
            file_name="file.txt",
            options=self.TempOptions(offset=4),
        )
        assert (
            request.json()
            == '{"document": "SGVsbG8gV29ybGQ0IQ==", "service_name": "QDS.TEST", "file_name": "file.txt", "options": {"offset": 4}}'
        )


class TestTransformDocumentResponse:
    def test_asdict_required_params(self):
        response = TransformDocumentResponse(
            document=encode_base64("Hello World Response2!")
        )
        response_dict = response.dict()
        assert len(response_dict.keys()) == 3
        assert response_dict["document"] == "SGVsbG8gV29ybGQgUmVzcG9uc2UyIQ=="
        assert response_dict["output"] is None
        assert response_dict["error"] is None

    def test_asdict_all_params(self):
        response = TransformDocumentResponse(
            document=encode_base64("Hello World Response3!"),
            output=["OUTPUT 1", "OUTPUT 2"],
            error=["ERROR 1", "ERROR 2"],
        )
        response_dict = response.dict()
        assert len(response_dict.keys()) == 3
        assert response_dict["document"] == "SGVsbG8gV29ybGQgUmVzcG9uc2UzIQ=="
        assert response_dict["output"] == ["OUTPUT 1", "OUTPUT 2"]
        assert response_dict["error"] == ["ERROR 1", "ERROR 2"]

    def test_asjson_required_params(self):
        response = TransformDocumentResponse(
            document=encode_base64("Hello World Response4!")
        )
        assert (
            response.json()
            == '{"document": "SGVsbG8gV29ybGQgUmVzcG9uc2U0IQ==", "output": null, "error": null}'
        )

    def test_asjson_all_params(self):
        response = TransformDocumentResponse(
            document=encode_base64("Hello World Response5!"),
            output=["OUTPUT 1", "OUTPUT 2"],
            error=["ERROR 1", "ERROR 2"],
        )
        assert (
            response.json()
            == '{"document": "SGVsbG8gV29ybGQgUmVzcG9uc2U1IQ==", "output": ["OUTPUT 1", "OUTPUT 2"], "error": ["ERROR 1", "ERROR 2"]}'
        )


class TestListServicesResponse:
    def test_asdict(self):
        response = ListServicesResponse(
            services=[ServiceInfo(name="QDS.TEST"), ServiceInfo(name="QDS.ECHO")]
        )
        response_dict = response.dict()
        assert len(response_dict.keys()) == 1
        assert response_dict["services"] == [{"name": "QDS.TEST", "options": None}, {"name": "QDS.ECHO", "options": None}]

    def test_asjson(self):
        response = ListServicesResponse(
            services=[ServiceInfo(name="QDS.TEST"), ServiceInfo(name="QDS.ECHO")]
        )
        assert (
            response.json()
            == '{"services": [{"name": "QDS.TEST", "options": null}, {"name": "QDS.ECHO", "options": null}]}'
        )


class TestTransformDocumentPipeRequest:
    def test_asdict_required_params(self):
        request = TransformDocumentPipeRequest(
            document=encode_base64("Hello Pipe Request2!"),
            services=[ServiceInfo(name="QDS.ECHO")],
            file_name=None,
        )
        request_dict = request.dict()
        assert len(request_dict.keys()) == 3
        assert request_dict["document"] == "SGVsbG8gUGlwZSBSZXF1ZXN0MiE="
        assert request_dict["services"] == [{"name": "QDS.ECHO", "options": None}]
        assert request_dict["file_name"] is None

    def test_asdict_all_params(self):
        request = TransformDocumentPipeRequest(
            document=encode_base64("Hello Pipe Request3!"),
            services=[ServiceInfo(name="QDS.COUNT")],
            file_name="secret.txt",
        )
        request_dict = request.dict()
        assert len(request_dict.keys()) == 3
        assert request_dict["document"] == "SGVsbG8gUGlwZSBSZXF1ZXN0MyE="
        assert request_dict["services"] == [{"name": "QDS.COUNT", "options": None}]
        assert request_dict["file_name"] == "secret.txt"

    def test_asjson_required_params(self):
        request = TransformDocumentPipeRequest(
            document=encode_base64("Hello Pipe Request4!"),
            services=[ServiceInfo(name="QDS.CAESER")],
            file_name=None,
        )
        assert (
            request.json()
            == '{"document": "SGVsbG8gUGlwZSBSZXF1ZXN0NCE=", "services": [{"name": "QDS.CAESER", "options": null}], "file_name": null}'
        )

    def test_asjson_all_params(self):
        request = TransformDocumentPipeRequest(
            document=encode_base64("Hello Pipe Request5!"),
            services=[ServiceInfo(name="QDS.MAIL")],
            file_name="sec.txt",
        )
        assert (
            request.json()
            == '{"document": "SGVsbG8gUGlwZSBSZXF1ZXN0NSE=", "services": [{"name": "QDS.MAIL", "options": null}], "file_name": "sec.txt"}'
        )


# class TestTransformDocumentPipeResponse():
#     B64_HELLO_WORLD_PIPE_BACK = b64encode("Hello World Pipe Back!".encode("utf-8")).decode("utf-8")

#     def test_trans_document_validation_success(self):
#         response = TransformDocumentPipeResponse(trans_document=self.B64_HELLO_WORLD_PIPE_BACK, sender="QDS.TST")
#         print(vars(response))
#         assert response.trans_output == self.B64_HELLO_WORLD_PIPE_BACK
