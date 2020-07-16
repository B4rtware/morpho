from morpho.config import ServiceConfig
from morpho.server import Service
from typing import Callable
from morpho.consumer import RestWorkConsumer
import flask


class RestProxyConsumer(RestWorkConsumer):
    def __init__(self, work: Callable, config: ServiceConfig):
        super().__init__(work, config)
        self.app.before_request(self.capture_request)
        self.app.after_request(self.capture_response)

    def capture_request(self):
        print("Before")
        print(flask.request)

    def capture_response(self, response):
        print("After")
        print(response)

        return response

proxy = Service("PROXY", "1.0.1", protocols=[RestProxyConsumer], work=lambda x, y: x)

if __name__ == "__main__":
    proxy.run(50030)