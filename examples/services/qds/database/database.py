from pathlib import Path
from grpc import ServicerContext
from service.proto.dtaservice_pb2 import DocumentRequest
import sys

sys.path.append(str(Path(".").resolve()))
from service.server import DTAServer

import doctrans_py_swagger_client

from typing import Tuple, Optional

api_instance = doctrans_py_swagger_client.TracesApi(
    doctrans_py_swagger_client.ApiClient()
)


class QDS_DATABASE(DTAServer):
    version = "0.0.1"
    app_name = "DE.TU-Berlin.QDS.DATABASE"

    def work(
        self, request: DocumentRequest, context: ServicerContext
    ) -> Tuple[str, Optional[str]]:
        trace = doctrans_py_swagger_client.Trace(service_name="")

        try:
            api_response = api_instance.traces_create(trace)
            print(api_response)
        except doctrans_py_swagger_client.rest.ApiException as e:
            # TODO: log this output
            print(f"Exception when calling TracesApi->traces_create: {e}\n")

        return ("", None)


QDS_DATABASE.run()
