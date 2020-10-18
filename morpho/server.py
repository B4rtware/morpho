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
        consumers: Optional[List[Type[WorkConsumer]]] = None,
        worker: Optional[Worker] = None,
        register: bool = False,
        config: Optional[ServiceConfig] = None,
        type: DtaType = DtaType.SERVICE,
        options_type: Optional[Type[BaseModel]] = None,
    ):
        if consumers is None:
            consumers = [RestWorkConsumer]
        if config is None:
            # TODO: remove those asserts
            assert not name is None
            assert not version is None
            self.config = ServiceConfig(
                name=name,
                version=version,
                consumers=consumers,
                type=type,
                register=register,
            )
        else:
            self.config = config
        self.options_type = options_type

        self._should_stop = Event()
        self._worker = worker

    def run(
        self,
        service_name: Optional[str] = None,
        register: Optional[bool] = None,
        registrar_url: Optional[str] = None,
        ttl: Optional[int] = None,
        host_name: Optional[str] = None,
        # TODO: rename to port
        port_to_listen: Optional[int] = None,
        dta_type: Optional[DtaType] = None,
        is_ssl: Optional[bool] = None,
        consumers: Optional[List[Type[WorkConsumer]]] = None,
    ):
        """Class method which is used to invoke the server.
        """
        properties = {
            "register": register,
            "service_name": service_name,
            "registrar_url": registrar_url,
            "ttl": ttl,
            "host_name": host_name,
            "port_to_listen": port_to_listen,
            "type": dta_type,
            "is_ssl": is_ssl,
            "consumers": consumers,
        }
        properties["name"] = properties.pop("service_name")
        properties["should_register"] = properties.pop("register")
        for name, value in properties.items():
            if not value is None:
                setattr(self.config, name, value)

        if self.config.name == "UNKNOWN":
            log.warning("no application name was specified instead using: UNKNOWN!")

        # register at eureka server
        if self.config.should_register:
            eureka_client.init_registry_client(
                eureka_server=self.config.registrar_url,
                instance_host=self.config.host_name,
                app_name=self.config.name,
                instance_port=int(self.config.port_to_listen),
                instance_secure_port_enabled=self.config.is_ssl,
                metadata={"dtaType": self.config.type.value},
            )

        assert (
            self.config.consumers
        ), "Have you called super() on your Server implemenation?"
        # start protocol consumer
        for protocol in self.config.consumers:
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
            for setting in self.config.dict().items():
                print(f" |- {setting[0]:<15} - {setting[1]}")
            print("")
            for consumer in self.config.consumers:
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
