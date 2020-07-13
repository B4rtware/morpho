from morpho.rest.raw import (
    RawTransformDocumentPipeResponse,
    RawTransformDocumentResponse,
)
from typing import Tuple, cast
from morpho.server import Service
from morpho.consumer import RestWorkConsumer
from morpho.rest import Status
from morpho.rest.models import TransformDocumentPipeRequest, TransformDocumentRequest
import flask


class GatewayConsumer(RestWorkConsumer):
    def _transform_document(self) -> Tuple[RawTransformDocumentResponse, Status]:
        request_model = TransformDocumentRequest(**flask.request.json)
        result = self.client.transform_document(**request_model.dict())
        return cast(RawTransformDocumentResponse, result.dict()), Status.OK

    def _transform_document_pipe(
        self,
    ) -> Tuple[RawTransformDocumentPipeResponse, Status]:
        request_model = TransformDocumentPipeRequest(**flask.request.json)
        result = self.client.transform_document_pipe(**request_model.dict())
        return cast(RawTransformDocumentPipeResponse, result.dict()), Status.OK


# TODO: implement ability to set worker to None
gateway = Service(
    name="crypto-gateway", version="0.0.1", protocols=[GatewayConsumer], worker=lambda x: x
)

if __name__ == "__main__":
    gateway.run(50000)
