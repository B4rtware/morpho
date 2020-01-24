from dataclasses import dataclass
import dataclasses
from pathlib import Path
import sys
import json
from typing import Optional, Tuple
import grpc
import py_eureka_client.eureka_client as eureka_client

sys.path.append(str(Path(".").resolve()))

from dtaservice.dtaservice_pb2 import TransformDocumentResponse
from dtaservice.dtaservice_pb2_grpc import DTAServerStub
from services.services import DTAServer

@dataclass
class CountResults():
    Bytes: int
    Lines: int
    Words: int

class QDS_PROXY(DTAServer):
    version = "0.0.1"
    app_name = "QDS.PROXY"

    def work(self, request, context) -> Tuple[str, Optional[str]]:
        # TODO: database call here
        pass

    def TransformDocument(self, request, context):
        #to = eureka_client.get_application("http://localhost:8761/eureka", request.service_name)
        print(f"wants to call: {request.service_name}")
        # forward message
        channel = grpc.insecure_channel("localhost:50052")
        stub = DTAServerStub(channel)
        result = stub.TransformDocument(request)
        # forward request to database service
        channel = grpc.insecure_channel("localhost:50053")
        stub = DTAServerStub(channel)
        result = stub.TransformDocument(request)
        print(result.trans_document)
        return TransformDocumentResponse(
            trans_document=result.trans_document,
            trans_output=result.trans_output,
            error=result.error
        )

QDS_PROXY.run(50051)