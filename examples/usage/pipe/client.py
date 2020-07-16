from morpho.rest.models import ServiceInfo, TransformDocumentPipeRequest
from morpho.client import Client, ClientConfig

# TODO: add default 
morpho = Client(ClientConfig("http://localhost:8761/eureka/"))

request = TransformDocumentPipeRequest(
    document="Document zum PIPEN",
    services= [
        ServiceInfo("ECHO", "1.0.1", None),
        ServiceInfo("LOWER", "1.2.3", None),
        ServiceInfo("REVERSE", "1.0.2", None)
    ]
)

response = morpho.transform_document_pipe(request)
print("output " + "-"*40)
print("| - document: {}".format(response.document))
print("| - output: {}".format(response.output))
print("| - error: {}".format(response.error))