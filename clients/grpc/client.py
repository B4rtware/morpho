import argparse
from dataclasses import dataclass
import py_eureka_client.eureka_client as eureka_client
# import logging as log
import grpc
import urllib
import sys
from pathlib import Path

sys.path.append(str(Path(".").resolve()))
from dtslog import log
from dtaservice.dtaservice_pb2_grpc import DTAServerStub
from dtaservice.dtaservice_pb2 import ListServiceRequest, DocumentRequest


parser = argparse.ArgumentParser()
parser.add_argument("--FileName", type=str, help="the file to be uploaded")
parser.add_argument(
    "--EurekaURL",
    type=str,
    help="if set the indicated eureka server will be used to find DTA-GW",
)
parser.add_argument("--ServiceName", type=str, help="The service to be used")
parser.add_argument(
    "--ServiceAddress", type=str, help="Address and port of the server to connect"
)
parser.add_argument(
    "--ListServices", help="List all the services accessible", action="store_true",
)
parser.add_argument(
    "--LogLevel",
    type=str,
    help="Log level, one of panic, fatal, error, warn or warning, info, debug, trace",
    choices=(
        "CRITICAL",
        "FATAL",
        "ERROR",
        "WARNING",
        "WARN",
        "INFO",
        "DEBUG",
        "NOTSET",
    ),
    default="INFO",
)


@dataclass
class Config:
    FileName: str = ""
    EurekaURL: str = ""
    ServiceName: str = ""
    ServiceAddress: str = ""
    ListServices: bool = False
    LogLevel: str = ""


DTA_GW_ID = "DE.TU-BERLIN.QDS.GW-INTERNAL"


if __name__ == "__main__":
    config = Config(
        ServiceName="DE.TU-BERLIN.QDS.ECHO", EurekaURL="http://localhost:8761/eureka"
    )

    # parse to fill the configuration
    args = parser.parse_args()
    for arg in vars(args).items():
        if arg[1]:
            setattr(config, arg[0], arg[1])

    log.getLogger().setLevel(log._nameToLevel[config.LogLevel])
    log.info(f"Requesting service {config.ServiceName}")

    # We have to identify the server to contact
    # We have to possibilities
    #  a) via registry (the normal case)
    #  b) direct, more for testing purposes

    #  a) via resolver is assumed if no server is given
    #  - contact the well-known resolver

    if config.ServiceAddress == "":
        log.info(f"Will contact registry at {config.EurekaURL}")

        service = None
        try:
            service = eureka_client.get_application(
                config.EurekaURL, config.ServiceName
            )
        except urllib.error.HTTPError as e:
            if e.code == 404:
                log.info(f"Could not find the service {config.ServiceName} at eureka")

        if service is None:
            log.info(f"Looking for a gateway {DTA_GW_ID}")

            try:
                service = eureka_client.get_application(config.EurekaURL, DTA_GW_ID)
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    log.info(f"Could not find a gateway {DTA_GW_ID} at eureka")
                    log.error(
                        f"Could not connect to service {config.ServiceName} or to gateway {DTA_GW_ID}"
                    )
                    exit(1)
        else:
            # check for available proxy
            #proxy_instances = [instance for instance in service.instances if instance.metadata.get("DTA-Type", "") == "PROXY"]
            #proxy_found = len(proxy_instances) > 0
            # use proxy if we found one
            #if proxy_found:
            #    service = proxy_instances
            #    log.info(f"found available proxy")
            # TODO: maybe use caching so discorcy client 
            try:
                service = eureka_client.get_application(config.EurekaURL, config.ServiceName + ".PROXY")
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    log.info(f"no proxy was found for app name {config.ServiceName}")
            
            config.ServiceAddress = (
                f"{service.instances[0].ipAddr}:{service.instances[0].port.port}"
            )
            log.info(
                f"Will contact {config.ServiceAddress} for service for {config.ServiceName}"
            )

    # open grpc connection channel
    channel = grpc.insecure_channel(config.ServiceAddress)
    if not channel:
        log.error(f"Did not connect to {config.ServiceName}")
        channel.close()
        exit(1)
    stub = DTAServerStub(channel)

    # list avialable services
    response = stub.ListServices(ListServiceRequest())
    print(response)
    if response is None:
        log.error("could not list services")
        exit(1)

    # read content from file
    assert config.FileName != ""
    file_path = Path(config.FileName)
    if not file_path.exists():
        log.error(f"Specified file {config.FileName} does not exist")
        exit(1)

    with file_path.open("r") as file:
        document = file.read()

    response = stub.TransformDocument(
        DocumentRequest(
            service_name=config.ServiceName,
            file_name=config.FileName,
            document=document.encode(),
        )
    )

    print(response.trans_document)

