from importlib import import_module
from typing import List
from morpho.consumer import RestWorkConsumer
from morpho.config import ServiceConfig
import click
import sys

from morpho.types import DtaType

str_to_dta_type = {"service": DtaType.SERVICE, "gateway": DtaType.GATEWAY}
str_to_consumer = {"rest": RestWorkConsumer}


@click.group()
def cli(**kwargs):
    pass


# TODO: implement yaml option type
@cli.command()
@click.option(
    "--type",
    type=click.Choice(["json"]),
    help="Type for the output format of the configuration string",
)
def config(type: str):
    if type == "json":
        print(ServiceConfig().json(by_alias=True, indent=4))
    else:
        print(ServiceConfig().json(by_alias=True, indent=4))


@cli.command()
# fmt: off
@click.argument("service")
@click.option("--register", is_flag=True, help="Register the service with an eureka server")
@click.option("--registrar-url", type=str, help="Registry URL")
@click.option("--ttl", type=int, help="Time in seconds to register at registrar")
@click.option("--host-name", type=str, help="If provided will be used as hostname, else automatically derived.")
@click.option("--service-name", type=str, help="ID of the service as e.g. 'DOC.TXT.COUNT.'")
@click.option("--port-to-listen", type=int, help="On which port to listen for this service.")
@click.option("--type", type=click.Choice(["service", "gateway"]), help="One of Gateway or Service. Service is assumed if not provided.")
@click.option("--is-ssl", is_flag=True, help="Can the service be reached via SSL.")
@click.option("--protocols", type=click.Choice(["rest"]), multiple=True, help="Which protocol should be used by the server.")
# fmt: on
def serve(service: str, **kwargs):
    sys.path.insert(0, ".")
    module, func = service.split(":")
    service_module = import_module(module)
    protocols: List[str] = kwargs.pop("protocols")
    consumers = [str_to_dta_type[protocol] for protocol in protocols]
    if not kwargs["type"] is None:
        kwargs["type"] = str_to_dta_type[kwargs.pop("type")]
    kwargs["dta_type"] = kwargs.pop("type")
    # TODO: currently empty protocols will be converted to None
    if consumers == []:
        consumers = None

    getattr(service_module, func).run(**dict(**kwargs, consumers=consumers))


def run():
    cli(auto_envvar_prefix="MORPHO")

