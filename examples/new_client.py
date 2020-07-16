
from morpho.consumer import RestWorkConsumer


o = """
{
    offset: {
        type: int,
        max: 10,
        min: 0
    }
}
"""


options = Options(".options.json")


c = """
{
    name: "QDS.TEST",
    version: "1.0.1",
    protocols: [
        "rest", "grpc"
    ]
}
"""

service = Service(
    name = "QDS.TEST",
    version = "1.0.1",
    protocols = [
        RestWorkConsumer,
        GrpcWorkConsumer
    ]
)

@service.work
def work(self):
    pass

if __name__ == "__main__":
    service.run()