import dataclasses
from pathlib import Path
import inspect
import argparse
import sys
import py_eureka_client.eureka_client as eureka_client
import grpc
import concurrent.futures as futures
import time

# also need to setup correct launch.json in vscode to prevent lint errors
sys.path.append("../../")

import dtaservice.doctransserver as pb
import dtaservice.dtaservice_pb2_grpc as dtaservice_pb2_grpc
import dtaservice.dtaservice_pb2 as dtaservice_pb2

parser = argparse.ArgumentParser()
parser.add_argument_group("Registrar")
parser.add_argument("--RegistrarURL",  type=str, help="Registry URL")
parser.add_argument("--RegistrarUser", type=str, help="Registry User, no user used if not provided")
# parser.add_argument("--RegistrarPwd-pwd",  type=str, help="Registry User Password, no password used if not provided")
parser.add_argument("--TTL",            type=int, help="Time in seconds to reregister at Registrar.")
parser.add_argument_group("Service")
parser.add_argument("--HostName",      type=str, help="If provided will be used as hostname, else automatically derived.")
parser.add_argument("--AppName",       type=str, help="ID of the service as e.g. 'DOC.TXT.COUNT.'")
parser.add_argument("--PortToListen", type=str, help="On which port to listen for this service.")
parser.add_argument("--DtaType",       type=str, help="One of Gateway or Service. Service is assumed if not provided.")
parser.add_argument("--IsSSL",         type=str, help="Can the service be reached via SSL.")
parser.add_argument_group("Generic")
parser.add_argument("--LogLevel",      type=int, help="Log level, one of panic, fatal, error, warn or warning, info, debug, trace")
parser.add_argument("--CfgFile",       type=str, help="The config file to use")
parser.add_argument("--Init",           help="Create a default config file as defined by cfg-file, if set. If not set ~/.dta/<AppName>/config.json will be created.", action='store_true')


version = ".1"

VERSION = "0.0" + version + "-src"

APP_NAME = "DE.TU-BERLIN.QDS.ECHO"

def work(input):
    return input

class QDS_ECHO(dtaservice_pb2_grpc.DTAServerServicer):
    def TransformDocument(self, request: dtaservice_pb2.DocumentRequest, context):
        # print("TRACE: QDS_ECHO | file_name: {} | document: {} | service_name {}".format(request.file_name, request.document, request.service_name))
        l = work(request.document)
        return dtaservice_pb2.TransformDocumentReply(
            trans_document = l,
            trans_output = l.decode(),
            error = None
        )

    def ListServices(self, request: dtaservice_pb2.ListServiceRequest, context):
        services = [APP_NAME]
        return dtaservice_pb2.ListServicesResponse(services = services)

def main():
    working_home_dir = Path.home()

    dts = pb.DocTransServer(
        RegistrarURL="http://127.0.0.1:8761/eureka",
        PortToListen="50051"
    )

    # parse to fill the configuration
    args = parser.parse_args()
    for arg in vars(args).items():
        if arg[1]:
            setattr(dts, arg[0], arg[1])

    if dts.Init:
        dts.new_config_file()

    # max_port_seeks = 20
    # # dts.create_listener(max_port_seeks)

    # s = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # s.add_insecure_port("[::]:50051")
    # #s.start()

    # sa = QDS_ECHO()
    # dtaservice_pb2_grpc.add_DTAServerServicer_to_server(sa, s)
    # s.start()

    # while True:
    #     print("idling...")
    #     time.sleep(5)




main()

