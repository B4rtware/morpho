from pathlib import Path
import sys
from typing import Optional, Tuple
import grpc
import py_eureka_client.eureka_client as eureka_client

sys.path.append(str(Path(".").resolve()))
from dtslog import log
from dtaservice.dtaservice_pb2 import TransformDocumentResponse
from dtaservice.dtaservice_pb2_grpc import DTAServerStub
from dtaservice.server import DTAServer


class QDS_PROXY(DTAServer):
    version = "0.0.1"
    app_name = "DE.TU-BERLIN.QDS.PROXY"

    def __init__(self) -> None:
        super().__init__()

        self.registered_proxy_app_instances = []

    def work(self, request, context) -> Tuple[str, Optional[str]]:
        # TODO: database call here
        pass

    def TransformDocument(self, request, context):
        # TODO: implement internal service communication protocol using grpc (sendEvent("register_proxy", "..."))
        # let services be registed by the proxy to route to it self
        if (
            request.document.decode()
            == "REGISTER ME - id:59e46078-6ca5-4f0b-9732-e6fdf5f5a49e"
        ):
            self.registered_proxy_app_instances.append(
                eureka_client.init_registry_client(
                    eureka_server=self.dts.RegistrarURL,
                    instance_id=self.dts.HostName,
                    app_name=request.service_name + ".PROXY",
                    instance_port=int(self.dts.PortToListen),
                    instance_secure_port_enabled=self.dts.IsSSL,
                    metadata={"DTA-Type": "PROXY_SERVICE"},
                )
            )
            log.info(f"registered {request.service_name + '.PROXY'}")
            return TransformDocumentResponse(
                trans_document="OK - id:59e46078-6ca5-4f0b-9732-e6fdf5f5a49e".encode()
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
