from morpho.util import decode_base64
from morpho.types import ServiceType
from morpho.config import BaseConfig, ServerConfig
from morpho.rest.models import RawListServicesResponse, RawTransformDocumentResponse
from morpho.rest import Status
from typing import Callable, Optional, Tuple, cast
from morpho.consumer import RestWorkConsumer
from morpho.server import Server, run_app
import flask

class RestProxyConsumer(RestWorkConsumer):
    def __init__(self, work: Callable, config: ServerConfig):
        super().__init__(work, config)
        self.app.before_request(self.capture_request)
        self.app.after_request(self.capture_response)

    def capture_request(self):
        pass
        # print("Before")
        # print(flask.request)

    def capture_response(self, response):
        pass
        # print("After")
        # print(response)

        return response
    
    # def _transform_document(self) -> Tuple[RawTransformDocumentResponse, Status]:
    #     print("+-------------+")
    #     print("|-- Request --|")
    #     print("+-------------+")
    #     r: flask.Request = cast(flask.Request, flask.request)
    #     print("Cookies       : {}".format(r.cookies))
    #     print("Date          : {}".format(r.date))
    #     print("Args          : {}".format(r.args))
    #     print("Authorization : {}".format(r.authorization))
    #     print("Data          : {}".format(r.data))
    #     print("Endpoint      : {}".format(r.endpoint))
    #     print("Content-Length: {}".format(r.content_length))

    #     print(" --- Morpho --- ")

    #     print("document      : {}".format(decode_base64(flask.request.json["document"])))
    #     print("service_name  : {}".format(flask.request.json["service_name"]))
    #     # print("options       : {}".format(flask.request.json["options"]))
    #     print("file_name     : {}".format(flask.request.json["file_name"]))
    #     response = super()._transform_document()
    #     print("")
    #     print("+--------------+")
    #     print("|-- Response --|")
    #     print("+--------------+")
    #     print("Status         : {}".format(response[1].value))

    #     print(" --- Morpho --- ")

    #     print("document       : {}".format(response[0]["document"]))
    #     print("output         : {}".format(response[0]["output"]))
    #     print("error          : {}".format(response[0]["error"]))

    #     return response

    # def _list_services(self) -> Tuple[RawListServicesResponse, Status]:
    #     self.client.list_services()
    #     print(flask.request)
    #     return super()._list_services()

@run_app(port=50000)
class TraceProxy(Server):

    version = "0.0.1"
    name = "PROXY"
    morpho_type = ServiceType.PROXY

    def __init__(self, config: Optional[ServerConfig]) -> None:
        super().__init__(config)
        self.protocols = {"rest": RestProxyConsumer}

    def work(self, document: str, options: Optional[BaseConfig]) -> str:
        return document

# TODO: put name into consumer !!!
# TODO: multiple servers how to handle port and ip discorvery on eureka?
# TODO: look into grpc service userfull or merge? add response class ?
service = Server(
    version = "0.0.1"
    name = "proxy"
    service_type = ServiceType
    protocols = [
        RestProxyConsumer
    ]
)


# return RestResponse()
# return GrpcResponse()

if __name__ == "__main__":
    service.run()
