from typing import List
from morpho.error import NoWorkerFunctionError
from morpho.rest.models import TransformDocumentRequest
import httpretty
from pydantic.main import BaseModel
import pytest

from morpho.config import ServiceConfig
from morpho.consumer import RestGatewayConsumer, RestGatewayServiceConfig, WorkConsumer
from morpho.types import Worker
from tests.unit.eureka_mock_data import (
    EUREKA_GET_APPS_RESPONSE_CAESER_PERMUTATION_VIGENERE,
    EUREKA_GET_APPS_RESPONSE_ONLY_CAESER,
    EUREKA_GET_APPS_RESPONSE_CAESER_PERMUATION_CRYPTOxGW,
    EUREKA_GET_APPS_RESPONSE_ECHO_COUNT_CRYPTOxGW,
)


class MockConsumer(WorkConsumer):
    def start(self) -> None:
        pass


@pytest.fixture
def consumer():
    yield MockConsumer(work=None, config=ServiceConfig(name="ECHO"), options_type=None)


@pytest.fixture
def consumer_eureka():
    yield MockConsumer(
        work=None, config=ServiceConfig(name="CAESER", register=True), options_type=None
    )


def test_list_services_no_eureka(consumer: MockConsumer):
    list_service_response = consumer.list_services()

    assert len(list_service_response.services) == 1
    assert list_service_response.services[0].name == "ECHO"


@httpretty.activate(allow_net_connect=False)
def test_list_services_with_eureka_and_three_apps(consumer_eureka: MockConsumer):
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8761/eureka/apps/",
        body=EUREKA_GET_APPS_RESPONSE_CAESER_PERMUTATION_VIGENERE,
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:50000/v1/service/options",
        body="{}",
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:50001/v1/service/options",
        body="{}",
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:50002/v1/service/options",
        body="{}",
        status=200,
    )

    list_services_response = consumer_eureka.list_services()

    # FIXME: maybe bad because what if the order changes?
    #        the test should not care in which order they are received
    assert len(list_services_response.services) == 3
    assert list_services_response.services[0].name == "CAESER"
    assert list_services_response.services[0].options == {}
    assert list_services_response.services[1].name == "PERMUTATION"
    assert list_services_response.services[1].options == {}
    assert list_services_response.services[2].name == "VIGENERE"
    assert list_services_response.services[2].options == {}


@httpretty.activate(allow_net_connect=False)
def test_list_services_with_eureka_and_no_other_apps(consumer_eureka: MockConsumer):
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8761/eureka/apps/",
        body=EUREKA_GET_APPS_RESPONSE_ONLY_CAESER,
        status=200,
    )

    list_services_response = consumer_eureka.list_services()
    assert len(list_services_response.services) == 1
    assert list_services_response.services[0].name == "CAESER"
    assert list_services_response.services[0].options == {}


@httpretty.activate(allow_net_connect=False)
def test_list_services_with_eureka_and_two_other_apps_and_one_gateway(
    consumer_eureka: MockConsumer,
):
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8761/eureka/apps/",
        body=EUREKA_GET_APPS_RESPONSE_CAESER_PERMUATION_CRYPTOxGW,
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:50000/v1/service/options",
        body="{}",
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:50001/v1/service/options",
        body="{}",
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:50002/v1/service/options",
        body="{}",
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:50002/v1/service/list",
        body="""{"services": [
                    {"name": "CAESER", "options": {}},
                    {"name": "PERMUTATION", "options": {}},
                    {"name": "CRYPTO.GW", "options": {}},
                    {"name": "CRYPTO.CRYPTOSIE", "options": {}}
                ]}""",
        status=200,
    )

    list_services_response = consumer_eureka.list_services()
    assert len(list_services_response.services) == 4
    assert list_services_response.services[0].name == "CAESER"
    assert list_services_response.services[0].options == {}
    assert list_services_response.services[1].name == "PERMUTATION"
    assert list_services_response.services[1].options == {}
    assert list_services_response.services[2].name == "CRYPTO.GW"
    assert list_services_response.services[2].options == {}
    assert list_services_response.services[3].name == "CRYPTO.CRYPTOSIE"
    assert list_services_response.services[3].options == {}


@httpretty.activate(allow_net_connect=False)
def test_list_services_with_eureka_and_two_other_apps_and_one_gateway_resolver():
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8761/eureka/apps/",
        body=EUREKA_GET_APPS_RESPONSE_ECHO_COUNT_CRYPTOxGW,
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:8762/eureka/apps/",
        body=EUREKA_GET_APPS_RESPONSE_CAESER_PERMUTATION_VIGENERE,
        status=200,
    )
    # CEASER PERMUTATION VEVENERE
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:50000/v1/service/options",
        body="{}",
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:50001/v1/service/options",
        body="{}",
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:50002/v1/service/options",
        body="{}",
        status=200,
    )
    # ECHO COUNT
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:50010/v1/service/options",
        body="{}",
        status=200,
    )
    httpretty.register_uri(
        httpretty.GET,
        "http://localhost:50011/v1/service/options",
        body="{}",
        status=200,
    )

    mock_rest_gateway_consumer = RestGatewayConsumer(
        work=None,
        config=RestGatewayServiceConfig(
            name="CRYPTO.GW",
            register=True,
            registrar_url="http://localhost:8761/eureka",
            resolver_url="http://localhost:8762/eureka",
        ),
        options_type=None,
    )

    list_service_response = mock_rest_gateway_consumer.list_services()
    assert len(list_service_response.services) == 6
    assert list_service_response.services[0].name == "CRYPTO.GW"
    assert list_service_response.services[0].options == {}
    assert list_service_response.services[1].name == "ECHO"
    assert list_service_response.services[1].options == {}
    assert list_service_response.services[2].name == "COUNT"
    assert list_service_response.services[2].options == {}
    assert list_service_response.services[3].name == "CRYPTO.CAESER"
    assert list_service_response.services[3].options == {}
    assert list_service_response.services[4].name == "CRYPTO.PERMUTATION"
    assert list_service_response.services[4].options == {}
    assert list_service_response.services[5].name == "CRYPTO.VIGENERE"
    assert list_service_response.services[5].options == {}


def test_options_no_options(consumer: MockConsumer):
    result = consumer.options()
    assert result == {}


def test_options_with_options():
    class Options(BaseModel):
        offset: int = 0

    consumer = MockConsumer(
        work=None,
        config=ServiceConfig(name="CAESER", options=Options),
        options_type=Options,
    )
    result = consumer.options()
    assert result == {
        "title": "Options",
        "type": "object",
        "properties": {"offset": {"title": "Offset", "default": 0, "type": "integer"}},
    }


def test_transform_document_no_worker(consumer: MockConsumer):
    request = TransformDocumentRequest(document="Hello World!", service_name="CAESER")

    with pytest.raises(NoWorkerFunctionError, match="No worker function specified!"):
        consumer.transform_document(request=request)


def mock_echo_worker(document: str):
    return document


def mock_append_worker(document: str):
    return "Appended" + document


def mock_echo_print_output_worker(document: str):
    print("transforming...")
    return document


@pytest.mark.parametrize(
    "worker_function,document,expected_document,expected_output",
    [
        (mock_echo_worker, "Document!", "Document!", []),
        (mock_append_worker, "Document", "AppendedDocument", []),
        (mock_echo_print_output_worker, "Doc", "Doc", ["transforming..."]),
    ],
)
def test_transform_document_with_worker(
    worker_function: Worker,
    document: str,
    expected_document: str,
    expected_output: List[str],
):
    consumer = MockConsumer(
        work=worker_function, config=ServiceConfig(name="ECHO"), options_type=None
    )
    request = TransformDocumentRequest(document=document, service_name="ECHO")
    result = consumer.transform_document(request=request)
    assert result.document == expected_document
    assert result.output == expected_output
    assert result.error == []

