import json

import httpretty
import pytest
import requests

from morpho.client import Client
from morpho.client import ClientConfig
from morpho.error import ServiceNotFoundError
from morpho.rest.models import (
    PipeService,
    TransformDocumentPipeRequest,
    TransformDocumentRequest,
)

# pylint: redefined-outer-name

# @pytest.fixture(scope="module")
# def app():
#     p = Process(target=uvicorn.run, kwargs={"app": "eureka_mock_server:app", "interface": "wsgi", "log_level": "error"}, daemon=True)
#     p.start()
#     yield
#     p.terminate()
#     print("waiting for close")
#     p.join()
#     # uvicorn.run("eureka_mock_server:app", interface="wsgi", log_level="error")


# def test_transform_document(app):
#     print(requests.get("http://localhost:8000/eureka/apps"))

# {
#     "applications": {
#         "versions__delta": "1",
#         "apps__hashcode": "UP_1_",
#         "application": [

EUREKA_GET_APPS_ECHO_RESPONSE = """
                    <application>
                        <name>ECHO</name>
                        <instance>
                            <instanceId>localhost:echo:50000</instanceId>
                            <hostName>localhost</hostName>
                            <app>ECHO</app>
                            <ipAddr>localhost</ipAddr>
                            <status>UP</status>
                            <overriddenstatus>UNKNOWN</overriddenstatus>
                            <port enabled="true">50000</port>
                            <securePort enabled="false">9443</securePort>
                            <countryId>1</countryId>
                            <dataCenterInfo class="com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo">
                            <name>MyOwn</name>
                            </dataCenterInfo>
                            <leaseInfo>
                            <renewalIntervalInSecs>30</renewalIntervalInSecs>
                            <durationInSecs>90</durationInSecs>
                            <registrationTimestamp>1600276007622</registrationTimestamp>
                            <lastRenewalTimestamp>1600276217630</lastRenewalTimestamp>
                            <evictionTimestamp>0</evictionTimestamp>
                            <serviceUpTimestamp>1600276006972</serviceUpTimestamp>
                            </leaseInfo>
                            <metadata>
                            <management.port>50000</management.port>
                            </metadata>
                            <homePageUrl>http://localhost:50000/</homePageUrl>
                            <statusPageUrl>http://localhost:50000/info</statusPageUrl>
                            <healthCheckUrl>http://localhost:50000/health</healthCheckUrl>
                            <secureHealthCheckUrl></secureHealthCheckUrl>
                            <vipAddress>echo</vipAddress>
                            <secureVipAddress>echo</secureVipAddress>
                            <isCoordinatingDiscoveryServer>false</isCoordinatingDiscoveryServer>
                            <lastUpdatedTimestamp>1600276007622</lastUpdatedTimestamp>
                            <lastDirtyTimestamp>1600276007162</lastDirtyTimestamp>
                            <actionType>ADDED</actionType>
                        </instance>
                        </application>"""

EUREKA_GET_APPS_COUNT_RESPONSE = """
                    <application>
                        <name>COUNT</name>
                        <instance>
                            <instanceId>localhost:count:50001</instanceId>
                            <hostName>localhost</hostName>
                            <app>COUNT</app>
                            <ipAddr>localhost</ipAddr>
                            <status>UP</status>
                            <overriddenstatus>UNKNOWN</overriddenstatus>
                            <port enabled="true">50001</port>
                            <securePort enabled="false">9443</securePort>
                            <countryId>1</countryId>
                            <dataCenterInfo class="com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo">
                            <name>MyOwn</name>
                            </dataCenterInfo>
                            <leaseInfo>
                            <renewalIntervalInSecs>30</renewalIntervalInSecs>
                            <durationInSecs>90</durationInSecs>
                            <registrationTimestamp>1600276007622</registrationTimestamp>
                            <lastRenewalTimestamp>1600276217630</lastRenewalTimestamp>
                            <evictionTimestamp>0</evictionTimestamp>
                            <serviceUpTimestamp>1600276006972</serviceUpTimestamp>
                            </leaseInfo>
                            <metadata>
                            <management.port>50001</management.port>
                            </metadata>
                            <homePageUrl>http://localhost:50001/</homePageUrl>
                            <statusPageUrl>http://localhost:50001/info</statusPageUrl>
                            <healthCheckUrl>http://localhost:50001/health</healthCheckUrl>
                            <secureHealthCheckUrl></secureHealthCheckUrl>
                            <vipAddress>echo</vipAddress>
                            <secureVipAddress>echo</secureVipAddress>
                            <isCoordinatingDiscoveryServer>false</isCoordinatingDiscoveryServer>
                            <lastUpdatedTimestamp>1600276007622</lastUpdatedTimestamp>
                            <lastDirtyTimestamp>1600276007162</lastDirtyTimestamp>
                            <actionType>ADDED</actionType>
                        </instance>
                        </application>"""


def raise_connection_error(*args, **kwargs):
    raise requests.exceptions.ConnectionError


@pytest.fixture(scope="function")
def client():
    config = ClientConfig(registrar_url="http://localhost:8761/eureka")
    yield Client(config)


@httpretty.activate(allow_net_connect=False)
def test_list_services(client: Client) -> None:
    httpretty.register_uri(
        method=httpretty.GET,
        uri="http://localhost:8761/eureka/apps/ECHO",
        body=EUREKA_GET_APPS_ECHO_RESPONSE,
        status=200,
    )

    httpretty.register_uri(
        method=httpretty.GET,
        uri="http://localhost:50000/v1/service/list",
        body=json.dumps({"services": [{"name": "ECHO"}]}),
        status=200,
    )

    response = client.list_services("ECHO")

    assert len(response.services) == 1
    service = response.services[0]
    assert service.name == "ECHO"


@httpretty.activate(allow_net_connect=False)
def test_list_services_no_service(client: Client) -> None:
    httpretty.register_uri(
        method=httpretty.GET, uri="http://localhost:8761/eureka/apps/ECHO", status=404,
    )

    with pytest.raises(ServiceNotFoundError, match="No service named <ECHO>"):
        client.list_services("ECHO")


@httpretty.activate(allow_net_connect=False)
def test_list_services_with_instance_address(client: Client) -> None:
    httpretty.register_uri(
        method=httpretty.GET,
        uri="http://localhost:50000/v1/service/list",
        body=json.dumps({"services": [{"name": "ECHO"}]}),
        status=200,
    )

    response = client.list_services("ECHO", instance_address="localhost:50000")

    assert len(response.services) == 1
    service = response.services[0]
    assert service.name == "ECHO"


def test_list_services_with_instance_address_no_service(
    monkeypatch, client: Client
) -> None:
    monkeypatch.setattr("morpho.client.requests.get", raise_connection_error)

    with pytest.raises(requests.exceptions.ConnectionError):
        client.list_services("ECHO", instance_address="localhost:50000")


# TODO: test other status code than 200


@httpretty.activate(allow_net_connect=False)
def test_transform_document(client: Client) -> None:
    httpretty.register_uri(
        method=httpretty.GET,
        uri="http://localhost:8761/eureka/apps/ECHO",
        body=EUREKA_GET_APPS_ECHO_RESPONSE,
        status=200,
    )

    httpretty.register_uri(
        method=httpretty.POST,
        uri="http://localhost:50000/v1/document/transform",
        body=json.dumps(
            {
                "document": "Hello World!",
                "output": ["transforming document <simpletext.txt> ..."],
                "error": ["Unknown Exception"],
            }
        ),
        status=200,
    )

    response = client.transform_document(
        TransformDocumentRequest(
            document="Hello world!",
            service_name="ECHO",
            file_name="simpletext.txt",
            options={"offset": 5, "debug": True},
        )
    )

    assert not response is None
    assert response.document == "Hello World!"
    assert not response.output is None
    assert len(response.output) == 1
    assert response.output == ["transforming document <simpletext.txt> ..."]
    assert response.error == ["Unknown Exception"]


@httpretty.activate(allow_net_connect=False)
def test_transform_document_no_service(client: Client) -> None:
    httpretty.register_uri(
        method=httpretty.GET, uri="http://localhost:8761/eureka/apps/ECHO", status=404,
    )

    with pytest.raises(ServiceNotFoundError, match="No service named <ECHO>"):
        client.transform_document(
            TransformDocumentRequest(
                document="Hello world!",
                service_name="ECHO",
                file_name="simpletext.txt",
                options={"offset": 5, "debug": True},
            )
        )


@httpretty.activate(allow_net_connect=False)
def test_transform_document_with_instance_address(client: Client) -> None:
    httpretty.register_uri(
        method=httpretty.POST,
        uri="http://localhost:50000/v1/document/transform",
        body=json.dumps(
            {
                "document": "Hello Worlds!",
                "output": ["transforming document <simpletext.txt> ...", "lol"],
                "error": ["Unknown Exceptions"],
            }
        ),
        status=200,
    )

    response = client.transform_document(
        TransformDocumentRequest(
            document="Hello world!",
            service_name="ECHO",
            file_name="simpletext.txt",
            options={"offset": 5, "debug": True},
        ),
        instance_address="localhost:50000",
    )

    assert not response is None
    assert response.document == "Hello Worlds!"
    assert not response.output is None
    assert len(response.output) == 2
    assert response.output == ["transforming document <simpletext.txt> ...", "lol"]
    assert response.error == ["Unknown Exceptions"]


def test_transform_document_with_instance_address_no_service(monkeypatch) -> None:
    config = ClientConfig(registrar_url="http://localhost:8761/eureka")
    client = Client(config)

    monkeypatch.setattr("morpho.client.requests.post", raise_connection_error)

    with pytest.raises(requests.exceptions.ConnectionError):
        client.transform_document(
            TransformDocumentRequest(
                document="Hello world!",
                service_name="ECHO",
                file_name="simpletext.txt",
                options={"offset": 5, "debug": True},
            ),
            instance_address="localhost:50000",
        )


@httpretty.activate(allow_net_connect=False)
def test_transform_document_pipe(client: Client) -> None:
    httpretty.register_uri(
        method=httpretty.GET,
        uri="http://localhost:8761/eureka/apps/ECHO",
        body=EUREKA_GET_APPS_ECHO_RESPONSE,
        status=200,
    )

    httpretty.register_uri(
        method=httpretty.POST,
        uri="http://localhost:50000/v1/document/transform-pipe",
        body=json.dumps(
            {
                "document": "Hello Worlds!",
                "output": ["transforming document <simpletext.txt> ...", "lol"],
                "error": ["Unknown Exceptions"],
                "last_transformer": "COUNT",
            }
        ),
        status=200,
    )

    response = client.transform_document_pipe(
        request=TransformDocumentPipeRequest(
            document="Hello World",
            services=[PipeService(name="ECHO"), PipeService(name="COUNT")],
        )
    )

    assert response.document == "Hello Worlds!"
    assert response.last_transformer == "COUNT"
    assert not response.output is None
    assert not response.error is None
    assert len(response.output) == 2
    assert len(response.error) == 1


@httpretty.activate(allow_net_connect=False)
def test_transform_document_pipe_no_service(client: Client) -> None:
    httpretty.register_uri(
        method=httpretty.GET, uri="http://localhost:8761/eureka/apps/ECHO", status=404,
    )

    with pytest.raises(ServiceNotFoundError, match="No service named <ECHO>"):
        client.transform_document_pipe(
            request=TransformDocumentPipeRequest(
                document="Hello World",
                services=[PipeService(name="ECHO"), PipeService(name="COUNT")],
            )
        )


@httpretty.activate(allow_net_connect=False)
def test_transform_document_pipe_with_instance_address(client: Client) -> None:
    httpretty.register_uri(
        method=httpretty.POST,
        uri="http://localhost:50000/v1/document/transform-pipe",
        body=json.dumps(
            {
                "document": "Hello World!!",
                "output": ["transforming document <simpletext.txt> ...", "lol"],
                "error": ["Unknown Exceptions"],
                "last_transformer": "COUNT",
            }
        ),
        status=200,
    )

    response = client.transform_document_pipe(
        request=TransformDocumentPipeRequest(
            document="Hello World",
            services=[PipeService(name="ECHO"), PipeService(name="COUNT")],
        ),
        instance_address="localhost:50000",
    )

    assert response.document == "Hello World!!"
    assert response.last_transformer == "COUNT"
    assert not response.output is None
    assert not response.error is None
    assert len(response.output) == 2
    assert len(response.error) == 1


def test_transform_document_pipe_with_instance_address_no_service(
    monkeypatch, client: Client
) -> None:
    monkeypatch.setattr("morpho.client.requests.post", raise_connection_error)

    with pytest.raises(requests.exceptions.ConnectionError):
        client.transform_document(
            TransformDocumentRequest(
                document="Hello world!",
                service_name="ECHO",
                file_name="simpletext.txt",
                options={"offset": 5, "debug": True},
            ),
            instance_address="localhost:50000",
        )


@httpretty.activate(allow_net_connect=False)
def test_get_options(client: Client) -> None:
    httpretty.register_uri(
        method=httpretty.GET,
        uri="http://localhost:8761/eureka/apps/ECHO",
        body=EUREKA_GET_APPS_ECHO_RESPONSE,
        status=200,
    )

    httpretty.register_uri(
        method=httpretty.GET,
        uri="http://localhost:50000/v1/service/options",
        body=json.dumps(
            {
                "properties": {
                    "offset": {"default": 0, "title": "Offset", "type": "integer"}
                },
                "title": "Options",
                "type": "object",
            }
        ),
        status=200,
    )

    response = client.get_options("ECHO")
    assert response == {
        "properties": {"offset": {"default": 0, "title": "Offset", "type": "integer"}},
        "title": "Options",
        "type": "object",
    }


@httpretty.activate(allow_net_connect=False)
def test_get_options(client: Client) -> None:
    httpretty.register_uri(
        method=httpretty.GET, uri="http://localhost:8761/eureka/apps/ECHO", status=404,
    )

    with pytest.raises(ServiceNotFoundError, match="No service named <ECHO>"):
        client.get_options("ECHO")


@httpretty.activate(allow_net_connect=False)
def test_get_options_with_instance_address(client: Client) -> None:
    httpretty.register_uri(
        method=httpretty.GET,
        uri="http://localhost:50000/v1/service/options",
        body=json.dumps(
            {
                "properties": {
                    "offset": {"default": 0, "title": "Offset", "type": "string"}
                },
                "title": "Options",
                "type": "object",
            }
        ),
        status=200,
    )

    response = client.get_options("ECHO", instance_address="localhost:50000")
    assert response == {
        "properties": {"offset": {"default": 0, "title": "Offset", "type": "string"}},
        "title": "Options",
        "type": "object",
    }


def test_get_options_with_instance_address_no_service(
    monkeypatch, client: Client
) -> None:
    monkeypatch.setattr("morpho.client.requests.get", raise_connection_error)

    with pytest.raises(requests.exceptions.ConnectionError):
        client.get_options("ECHO", instance_address="localhost:50000")
