from morpho.client import Client
from morpho.client import ClientConfig

morpho = Client(ClientConfig("http://localhost:8761/eureka/"))

response = morpho.transform_document(
    "This is a Document!",
    service_name="DE.TU-BERLIN.ECHO"
)

print("output " + "-"*40)
print("| - document: {}".format(response.document))
print("| - output: {}".format(response.output))
print("| - error: {}".format(response.error))

