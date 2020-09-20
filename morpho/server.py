""" This module contains the server which implements the base functionality for a service.

It also contains the raw responses and request types.

Warning:
    This might change in future versions.
"""
import argparse
from morpho.types import DtaType, Worker
import sys
from threading import Event
from typing import List, Optional, Type

import logging
import colorama as cr
import py_eureka_client.eureka_client as eureka_client

from pydantic import BaseModel

from morpho.config import ServiceConfig
from morpho.consumer import RestGatewayConsumer, RestWorkConsumer, WorkConsumer

cr.init()

log = logging.getLogger(__name__)

# TODO: put parser in function parse or something like main or so
# TODO: verify that all options are used or at least output a warning
# fmt: off
# pylint: disable=line-too-long
parser = argparse.ArgumentParser() # pylint: disable=invalid-name

parser.add_argument_group("Registrar")
parser.add_argument("--register", action="store_true", help="Register service with EUREKA, if set")
parser.add_argument("--registrar-url", type=str, help="Registry URL")
parser.add_argument("--registrar-user", type=str, help="Registry User, no user used if not provided")
parser.add_argument("--registrar-password", type=str, help="Registry User Password, no password used if not provided")
parser.add_argument("--ttl", type=int, help="Time in seconds to reregister at Registrar.")

parser.add_argument_group("Service")
parser.add_argument("--host-name", type=str, help="If provided will be used as hostname, else automatically derived.")
parser.add_argument("--app-name", type=str, help="ID of the service as e.g. 'DOC.TXT.COUNT.'")
parser.add_argument("--port-to-listen", type=str, help="On which port to listen for this service.")
parser.add_argument("--type", type=str, help="One of Gateway or Service. Service is assumed if not provided.")
parser.add_argument("--is-ssl", type=str, help="Can the service be reached via SSL.")
parser.add_argument("--rest", action="store_true", help="REST-API enabled on port 80, if set.")
parser.add_argument("--http-port", type=str, help="On which httpPort to listen for REST, if enableREST is set. Ignored otherwise.")
parser.add_argument("--protocols", type=str, nargs='+', help="Which protocol should be used by the server.", default="", choices=("rest", "grpc"))

parser.add_argument_group("Generic")
parser.add_argument("--log-level", type=str, help="Log level, one of panic, fatal, error, warn or warning, info, debug, trace", default="INFO", choices=("CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET"))
parser.add_argument("--config-file", type=str, help="The config file to use")
parser.add_argument("--init", help="Create a default config file as defined by cfg-file, if set. If not set ~/.morpho/<AppName>/config.json will be created.", action="store_true")
# pylint: enable=line-too-long

# fmt: on


class Service:
    def __init__(
        self,
        name: Optional[str] = None,
        version: Optional[str] = None,
        protocols: Optional[List[Type[WorkConsumer]]] = None,
        worker: Optional[Worker] = None,
        register: bool = False,
        config: Optional[ServiceConfig] = None,
        type: DtaType = DtaType.SERVICE,
        options_type: Optional[Type[BaseModel]] = None,
    ):
        if protocols is None:
            protocols = [RestWorkConsumer]
        if config is None:
            # TODO: remove those asserts
            assert not name is None
            assert not version is None
            self.config = ServiceConfig(
                name=name,
                version=version,
                protocols=protocols,
                type=type,
                register=register,
            )
        else:
            self.config = config
        self.options_type = options_type

        self._should_stop = Event()
        self._worker = worker

    def run(self, port: Optional[int] = None):
        """Class method which is used to invoke the server.
        """
        # working_home_dir = Path.home()
        # parse args and override with config
        args = parser.parse_args()
        for arg in vars(args).items():
            if arg[1]:
                setattr(self.config, arg[0], arg[1])

        if self.config.name == "UNKNOWN":
            log.warning("no application name was specified instead using: UNKNOWN!")

        if port is not None:
            self.config.port_to_listen = str(port)

        # parse arguments to populate the configuration
        # TODO: FIX CONFIG
        # args = parser.parse_args()
        # for arg in vars(args).items():
        #     if arg[1]:
        #         setattr(config, arg[0], arg[1])

        # log.getLogger().setLevel(self.config.log_level)

        # create new config file by saving the default values
        # TODO: reimplement save behavior
        # if self.config.init:
        #     self.config.save()
        #     log.info(
        #         "wrote example configuration file to %s. exiting.",
        #         self.config.config_file
        #     )
        #     sys.exit(0)
        #     return

        # register at eureka server
        if self.config.register:
            eureka_client.init_registry_client(
                eureka_server=self.config.registrar_url,
                instance_host=self.config.host_name,
                app_name=self.config.name,
                instance_port=int(self.config.port_to_listen),
                instance_secure_port_enabled=self.config.is_ssl,
                # TODO: change morpho type name to use the same from the rest specification
                metadata={"dtaType": self.config.type.value},
            )

        assert (
            self.config.protocols
        ), "Have you called super() on your Server implemenation?"
        # start protocol consumer
        for protocol in self.config.protocols:
            instance: WorkConsumer = protocol(
                self._worker, self.config, self.options_type
            )
            instance.start()

        # fmt: off
        if __debug__:
            # use -O flag to remove all debug branches out of the bytecode
            print("")
            print(" +-------" + "-" * len(self.config.name) + "-------+")
            print(f" |       {cr.Back.GREEN + cr.Fore.BLACK + self.config.name + cr.Back.RESET + cr.Fore.RESET}       |")
            print(" +-------" + "-" * len(self.config.name) + "-------+")
            for setting in self.config.as_dict().items():
                print(f" |- {setting[0]:<15} - {setting[1]}")
            print("")
            for consumer in self.config.protocols:
                print(f" [{consumer.__name__}] -> listening on port {self.config.port_to_listen}")
            print("")
            print(cr.Fore.YELLOW + "     You see this message because __debug__ is true.")
            print("     Use the -O flag to enable optimization `python -O`." + cr.Fore.RESET)
            print("")
        # fmt: on

        try:
            while not self._should_stop.is_set():
                self._should_stop.wait(0.5)
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    # from pydantic import BaseModel

    # class Options(BaseModel):
    #     offset: int

    # def work(document: str, option: Options) -> str:
    #     return document

    # service = Service(name="echo", version="1.0.1", worker=work, options_type=Options)

    # service.run(50000)

    # TODO: add morpho tag attribute like tag=gateway or type=gateway
    gateway = Service(
        name="gateway",
        version="0.0.1",
        protocols=[RestGatewayConsumer],
        type=DtaType.GATEWAY,
        register=True,
    )

    gateway.run(50010)
