from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from morpho.rest.models import OptionsErrorResponse


class ServiceNotFoundError(Exception):
    pass


class ServerTimeout(Exception):
    pass


class NoWorkerFunctionError(Exception):
    pass


class ServerValidationError(Exception):
    def __init__(self, properties: List["OptionsErrorResponse"]) -> None:
        self.code = 400
        self.properties = properties


class ServerGatewayTimeout(Exception):
    def __init__(self) -> None:
        super().__init__("Gateway Timeout")
        self.code = 504


class ServerUnexpectedError(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(message)
        self.code = code


class ServerOptionsValidationError(Exception):
    def __init__(self, error: "OptionsErrorResponse") -> None:
        super().__init__()
        self.error = error
