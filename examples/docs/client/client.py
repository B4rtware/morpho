from morpho.rest.models import TransformDocumentRequest
from morpho.client import Client
from morpho.client import ClientConfig


morpho = Client(
    ClientConfig("http://localhost:8761/eureka/")
)

request = TransformDocumentRequest(
    document="This is a Document!",
    service_name="Echo"
)

response = morpho.transform_document(request=request)
