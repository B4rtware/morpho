from pathlib import Path
import sys
from typing import Optional, Tuple
import grpc
from grpc import Channel, ServicerContext
import py_eureka_client.eureka_client as eureka_client

sys.path.append(str(Path(".").resolve()))

from dtslog import log
from service.proto.dtaservice_pb2 import DocumentRequest, TransformDocumentResponse
from service.proto.dtaservice_pb2_grpc import DTAServerStub
from service.server import DTAServer


class QDS_PROXY(DTAServer):
    version = "0.0.1"
    app_name = "DE.TU-BERLIN.QDS.PROXY"

    def __init__(self) -> None:
        super().__init__()

        self.registered_proxy_app_instances = []

    def work(self, request: DocumentRequest, context: ServicerContext) -> Tuple[str, Optional[str]]:
        # TODO: database call here
        return ("", None)


    def TransformDocument(self, request: DocumentRequest, context: ServicerContext) -> TransformDocumentResponse:
        # TODO: implement internal service communication protocol using grpc (sendEvent("register_proxy", "..."))
        # let services be registed by the proxy to route to it self
        if (
            request.document.decode()
            == "REGISTER ME - id:59e46078-6ca5-4f0b-9732-e6fdf5f5a49e"
        ):
            self.registered_proxy_app_instances.append(
                eureka_client.init_registry_client(
                    eureka_server=self.dtas_config.RegistrarURL,
                    instance_id=self.dtas_config.HostName,
                    app_name=request.service_name + ".PROXY",
                    instance_port=int(self.dtas_config.PortToListen),
                    instance_secure_port_enabled=self.dtas_config.IsSSL,
                    metadata={"DTA-Type": "PROXY_SERVICE"},
                )
            )
            log.info(f"registered {request.service_name + '.PROXY'}")
            return TransformDocumentResponse(
                trans_document="OK - id:59e46078-6ca5-4f0b-9732-e6fdf5f5a49e".encode(),
                trans_output=[],
                error=None
            )

        # TODO: consider using discovery client for caching
        to = eureka_client.get_application(
            "http://localhost:8761/eureka", request.service_name
        )
        log.info(f"wants to call: {request.service_name}")
        # remove self from the instance list
        # instances: List[eureka_client.Instance] = [
        #     instance
        #     for instance in to.instances
        #     if instance.port.port != self.dts.PortToListen
        # ]
        instance = to.instances[0]
        # forward message
        channel = grpc.insecure_channel(f"{instance.ipAddr}:{instance.port.port}")
        stub = DTAServerStub(channel)
        result = stub.TransformDocument(request)
        # FIXME: implement a observer pattern for proxy calls
        # FIXME: maybe rename database microservice to trace 
        database_service = eureka_client.get_application(
            "http://localhost:8761/eureka", "DE.TU-Berlin.QDS.DATABASE"
        )
        db_instance = database_service.instances[0]

        with grpc.insecure_channel(f"{db_instance.ipAddr}:{db_instance.port.port}") as channel:
            stub = DTAServerStub(channel)
            stub.TransformDocument(request)
        return TransformDocumentResponse(
            trans_document=result.trans_document,
            trans_output=result.trans_output,
            error=result.error,
        )


QDS_PROXY.run()
