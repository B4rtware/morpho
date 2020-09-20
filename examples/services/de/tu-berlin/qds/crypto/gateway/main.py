from morpho.types import DtaType
from morpho.consumer import RestGatewayConsumer
from morpho.server import Service

# TODO: add morpho tag attribute like tag=gateway or type=gateway
gateway = Service(name="crypto.gw", version="0.0.1", protocols=[RestGatewayConsumer], type=DtaType.GATEWAY)

if __name__ == "__main__":
    gateway.run(50000)
