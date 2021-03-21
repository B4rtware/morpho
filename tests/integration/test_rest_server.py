import subprocess
from pydantic.main import BaseModel
from morpho.consumer import RestWorkConsumer
from morpho.rest.models import (
    PipeService,
    TransformDocumentPipeRequest,
    TransformDocumentResponse,
)
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


def work(document: str) -> str:
    return document


def morpho_test_service(**kwargs):
    Service(
        name="TEST", version="0.0.1", consumers=[RestWorkConsumer], worker=work
    ).run(**kwargs)


# services for pipe


def work1(document: str):
    print("work1 called")
    return document + ",TEST1"


def work2(document: str):
    print("work2 called")
    return document + ",TEST2"


def work3(document: str):
    print("work3 called")
    return document + ",TEST3"


def morpho_test_service_1(**kwargs):
    Service(name="TEST1", version="0.0.1", worker=work1).run(**kwargs)


def morpho_test_service_2(**kwargs):
    Service(name="TEST2", version="0.0.1", worker=work2).run(**kwargs)


def morpho_test_service_3(**kwargs):
    Service(name="TEST3", version="0.0.1", worker=work3).run(**kwargs)


import requests


@pytest.fixture(scope="module")
def eureka_server():
    integration_path = Path(__file__).parent
    eureka_jar_path = integration_path.joinpath("eureka-0.0.1-SNAPSHOT.jar")
    if not eureka_jar_path.exists():
        raise FileNotFoundError(f"{eureka_jar_path} not found!")
    eureka_process = subprocess.Popen(
        ["java", "-jar", "{}/eureka-0.0.1-SNAPSHOT.jar".format(integration_path)]
    )
    # wait for eureka service to be ready
    for _ in range(MAX_RETRIES):
        try:
            result = requests.get("http://localhost:8761/actuator/health")
            break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)

    if not result.json()["status"] == "UP":
        eureka_process.terminate()
        return

    # launch services
    sys.argv = [sys.argv[0], "--register"]
    services = [
        morpho_test_service_1,
        morpho_test_service_2,
        morpho_test_service_3,
    ]
    service_ports = [50001 + index for index in range(3)]
    service_processes = [
        Process(
            target=run, kwargs={"port_to_listen": port, "register": True}, daemon=True,
        )
        for port, run in zip(service_ports, services)
    ]
    for service in service_processes:
        service.start()

    services_ready = set()
    for _ in range(MAX_RETRIES):
        for service_port in service_ports:
            if service_port in services_ready:
                continue
            try:
                result_service = requests.get(f"http://localhost:{service_port}/health")
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.RequestException as exception:
                SystemExit(exception)
            if (
                result_service.status_code == 200
                and result_service.json()["status"] == "UP"
            ):
                services_ready.add(service_port)
        if len(services_ready) == 3:
            break
        time.sleep(0.5)
    yield
    print("Module Session Scope Closed.")
    for process in service_processes:
        process.terminate()
        process.join()
        print(
            "process: "
            + str(process.ident)
            + " gracefully stopped with: "
            + str(process.exitcode)
        )
    eureka_process.terminate()


@pytest.fixture(scope="module")
def rest_server():
    # TODO: use a client to interact with the server to use more than one component?
    # remove all other program arguments and add the rest protocol
    # sys.argv = [sys.argv[0], "--protocols=rest"]
    sys.argv = [sys.argv[0]]

    # app = QDS_TEST
    service_process = Process(
        target=morpho_test_service, kwargs={"port_to_listen": 50000}, daemon=True
    )
    # app_thread = Thread(target=morpho_test_service.run, daemon=True)
    service_process.start()

    result = None
    for _ in range(MAX_RETRIES):
        try:
            result = requests.get("http://localhost:50000/health")
            break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)
    if (
        not result is None
        and result.status_code == 200
        and result.json()["status"] == "UP"
    ):
        yield
    else:
        raise Exception("Something went wrong while starting the service process!")
    service_process.terminate()


def test_rest_transform(rest_server):
    result = r.post(
        "http://127.0.0.1:50000/v1/document/transform",
        json={"document": "Hello World!", "service_name": "QDS.TEST"},
    )

    assert result.status_code == 200
    assert result.text
    transform_document_response = TransformDocumentResponse(**result.json())
    assert transform_document_response.document == "Hello World!"
    assert transform_document_response.error == []


def test_rest_list(rest_server):
    result = r.get("http://127.0.0.1:50000/v1/service/list")
    assert result.status_code == 200
    assert result.text
    document_response = result.json()
    assert document_response["services"] == [{"name": "TEST", "options": {}}]


def test_rest_transform_pipe(eureka_server):
    print("start pipe test")
    config = ClientConfig("http://127.0.0.1:8761/eureka")
    client = Client(config)
    response = client.transform_document_pipe(
        TransformDocumentPipeRequest(
            document="Hello World",
            services=[
                PipeService(name="TEST1"),
                PipeService(name="TEST2"),
                PipeService(name="TEST3"),
            ],
        )
    )
    assert response.document == "Hello World,TEST1,TEST2,TEST3"
    assert response.last_transformer == "TEST3"
