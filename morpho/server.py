""" This module contains the server which implements the base functionality for a service.

It also contains the raw responses and request types.

Warning:
    This might change in future versions.
"""
import logging
import sys
from threading import Event
from typing import List, Optional, Type

import colorama as cr
import py_eureka_client.eureka_client as eureka_client
from pydantic import BaseModel

from morpho.config import ServiceConfig
from morpho.consumer import (
    RestWorkConsumer,
    WorkConsumer,
)
from morpho.types import DtaType, Worker

cr.init()

log = logging.getLogger(__name__)


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

        # register at eureka server
        if self.config.register:
            eureka_client.init_registry_client(
                eureka_server=self.config.registrar_url,
                instance_host=self.config.host_name,
                app_name=self.config.name,
                instance_port=int(self.config.port_to_listen),
                instance_secure_port_enabled=self.config.is_ssl,
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
