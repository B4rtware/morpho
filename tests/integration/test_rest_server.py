import subprocess
from pydantic.main import BaseModel
from morpho.consumer import RestWorkConsumer
from morpho.rest.models import PipeService, TransformDocumentPipeRequest, TransformDocumentResponse
from morpho.client import Client, ClientConfig
import sys
import pytest
from threading import Thread
from multiprocessing import Process
from pathlib import Path

import requests as r

from morpho.server import Service
import time

# TODO: create fixture for rest server
# TODO: rename to test_rest.py

# retry for 60 seconds
MAX_RETRIES = 120


def work(document: str, _: BaseModel) -> str:
    return document

morpho_test_service = Service(name="TEST", version="0.0.1", protocols=[RestWorkConsumer], worker=work)

# services for pipe

def work1(document: str, _: BaseModel):
    print("work1 called")
    return document + ",TEST1"

def work2(document: str, _: BaseModel):
    print("work2 called")
    return document + ",TEST2"

def work3(document: str, _: BaseModel):
    print("work3 called")
    return document + ",TEST3"

def service1(port: int):
    Service(name="TEST1", version="0.0.1", worker=work1).run(port=port)
def service2(port: int):
    Service(name="TEST2", version="0.0.1", worker=work2).run(port=port)
def service3(port: int):
    Service(name="TEST3", version="0.0.1", worker=work3).run(port=port)
# morpho_test_service_1 = Service(name="TEST1", version="0.0.1", worker=work1)
# morpho_test_service_2 = Service(name="TEST2", version="0.0.1", worker=work2)
# morpho_test_service_3 = Service(name="TEST3", version="0.0.1", worker=work3)

import requests

@pytest.fixture(scope="module")
def eureka_server():
    integration_path = Path(__file__).parent
    p = subprocess.Popen(["java","-jar","{}/eureka-0.0.1-SNAPSHOT.jar".format(integration_path)])
    time.sleep(50)
    # result = requests.get("http://localhost:8761/actuator/health", verify=False)
    for i in range(10):
        try:
            result = requests.get("http://localhost:8761/actuator/health")
            break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
        

        if i == 9:
            print("error while starting eureka server...")

    if result.json()["status"] == "UP":
        sys.argv = [sys.argv[0], "--register"]
        # services = [morpho_test_service_1.run, morpho_test_service_2.run, morpho_test_service_3.run]
        services = [service1, service2, service3]
        processes = [Process(target=run, kwargs={"port": 50001+index}, daemon=True) for index, run in enumerate(services)]
        for process in processes:
            process.start()
        # spawn threads
        # print("wait some time")
        time.sleep(50)
        return p
    #     for process in processes:
    #         process.terminate()
    #         process.join()
    #         print("process: " + str(process.ident) + " gracefully stopped with: " + str(process.exitcode))
    # else:
    #     print("status is not up")
    # print(p.pid)
    # time.sleep(30)

    # p.terminate()

@pytest.fixture(scope="module")
def rest_server():
    # TODO: use a client to interact with the server to use more than one component?
    # remove all other program arguments and add the rest protocol
    # sys.argv = [sys.argv[0], "--protocols=rest"]
    sys.argv = [sys.argv[0]]

    # app = QDS_TEST
    app_thread = Thread(target=morpho_test_service.run, daemon=True)
    app_thread.start()

    retry = 0
    # wait until thread is avialable
    while retry < MAX_RETRIES:
        app_thread.join(timeout=0.5)
        if app_thread.is_alive():
            break
        retry += 1
    assert app_thread.is_alive()
    return app_thread


# TODO: optimize by using a config and retry if ping fails
def test_rest_transform(rest_server):
    # # TODO: use a client to interact with the server to use more than one component?
    # # remove all other program arguments and add the rest protocol
    # sys.argv = [sys.argv[0], "--protocols=rest"]

    # # app = QDS_TEST
    # app_thread = Thread(target=QDS_TEST.run, daemon=True)
    # app_thread.start()

    # app_thread.join(timeout=5)
    # assert app_thread.is_alive()

    result = r.post(
        "http://127.0.0.1:50000/v1/document/transform",
        json={
            "document": "Hello World!",
            "service_name": "QDS.TEST"
        },
    )

    assert result.status_code == 200
    assert result.text
    transform_document_response = TransformDocumentResponse(**result.json())
    assert transform_document_response.document == "Hello World!"
    assert transform_document_response.error == []


def test_rest_list(rest_server):
    # sys.argv = [sys.argv[0], "--protocols=rest"]

    # app_thread = Thread(target=QDS_TEST.run, daemon=True)
    # app_thread.start()

    # app_thread.join(timeout=5)
    # assert app_thread.is_alive()
    result = r.get("http://127.0.0.1:50000/v1/service/list")
    assert result.status_code == 200
    assert result.text
    document_response = result.json()
    assert document_response["services"] == [
        {"name": "TEST", "options": {}}
    ]


def test_rest_transform_pipe(eureka_server):
    print("start pipe test")
    config = ClientConfig("http://127.0.0.1:8761/eureka")
    client = Client(config)
    response = client.transform_document_pipe(TransformDocumentPipeRequest(
        document="Hello World",
        services=[
            PipeService(name="TEST1"),
            PipeService(name="TEST2"),
            PipeService(name="TEST3")
        ]
    ))
    assert response.document == "Hello World,TEST1,TEST2,TEST3"
    assert response.last_transformer == "TEST3"

    # FIXME: should not be terminated here
    eureka_server.terminate()

