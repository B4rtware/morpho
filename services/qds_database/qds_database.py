from pathlib import Path
import sys

sys.path.append(str(Path(".").resolve()))
from services.services import DTAServer

import doctrans_py_swagger

from typing import Tuple, Optional

api_instance = doctrans_py_swagger.TracesApi(doctrans_py_swagger.ApiClient())
    
class QDS_DATABASE(DTAServer):
    def work(self, request, context) -> Tuple[str, Optional[str]]:
        trace = doctrans_py_swagger.Trace(
            service_name=""
        )

        try:
            api_response = api_instance.traces_create(trace)
            print(api_response)
        except ApiException as e:
            # TODO: log this output
            print(f"Exception when calling TracesApi->traces_create: {e}\n")

        return (request.document, None)

QDS_DATABASE.run(50053)
