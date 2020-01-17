from dataclasses import dataclass
import dataclasses
from pathlib import Path
import sys
import json
from typing import Optional, Tuple
import grpc
import py_eureka_client.eureka_client as eureka_client

sys.path.append(str(Path(".").resolve()))

from dtaservice.dtaservice_pb2_grpc import DTAServerStub
from services.services import DTAServer

@dataclass
class CountResults():
    Bytes: int
    Lines: int
    Words: int

class QDS_PROXY(DTAServer):
    version = "0.0.1"
    app_name = "QDS.ECHO"

    def work(self, request, context) -> Tuple[str, Optional[str]]:
        # get ip
        #to = eureka_client.get_application("http://localhost:8761/eureka", request.service_name)
        # use ip
        print(f"wants to call: {request.service_name}")
        print(f"got context: {context}")
        channel = grpc.insecure_channel("localhost:50052")
        stub = DTAServerStub(channel)
        result = stub.TransformDocument(request)
        print(result)
        # eureka_client.get_applications("http://localhost:8761/eureka")
        return (result, None)

QDS_PROXY.run(50051)