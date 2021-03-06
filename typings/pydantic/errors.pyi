"""
This type stub file was generated by pyright.
"""

from decimal import Decimal
from pathlib import Path
from typing import Any, Set, Union
from .typing import AnyType

__all__ = ('PydanticTypeError', 'PydanticValueError', 'ConfigError', 'MissingError', 'ExtraError', 'NoneIsNotAllowedError', 'NoneIsAllowedError', 'WrongConstantError', 'BoolError', 'BytesError', 'DictError', 'EmailError', 'UrlError', 'UrlSchemeError', 'UrlSchemePermittedError', 'UrlUserInfoError', 'UrlHostError', 'UrlHostTldError', 'UrlExtraError', 'EnumError', 'IntegerError', 'FloatError', 'PathError', '_PathValueError', 'PathNotExistsError', 'PathNotAFileError', 'PathNotADirectoryError', 'PyObjectError', 'SequenceError', 'ListError', 'SetError', 'FrozenSetError', 'TupleError', 'TupleLengthError', 'ListMinLengthError', 'ListMaxLengthError', 'AnyStrMinLengthError', 'AnyStrMaxLengthError', 'StrError', 'StrRegexError', '_NumberBoundError', 'NumberNotGtError', 'NumberNotGeError', 'NumberNotLtError', 'NumberNotLeError', 'NumberNotMultipleError', 'DecimalError', 'DecimalIsNotFiniteError', 'DecimalMaxDigitsError', 'DecimalMaxPlacesError', 'DecimalWholeDigitsError', 'DateTimeError', 'DateError', 'TimeError', 'DurationError', 'HashableError', 'UUIDError', 'UUIDVersionError', 'ArbitraryTypeError', 'ClassError', 'SubclassError', 'JsonError', 'JsonTypeError', 'PatternError', 'DataclassTypeError', 'CallableError', 'IPvAnyAddressError', 'IPvAnyInterfaceError', 'IPvAnyNetworkError', 'IPv4AddressError', 'IPv6AddressError', 'IPv4NetworkError', 'IPv6NetworkError', 'IPv4InterfaceError', 'IPv6InterfaceError', 'ColorError', 'StrictBoolError', 'NotDigitError', 'LuhnValidationError', 'InvalidLengthForBrand', 'InvalidByteSize', 'InvalidByteSizeUnit')
class PydanticErrorMixin:
    code: str
    msg_template: str
    def __init__(self, **ctx: Any) -> None:
        self.__dict__ = ...
    
    def __str__(self) -> str:
        ...
    


class PydanticTypeError(PydanticErrorMixin, TypeError):
    ...


class PydanticValueError(PydanticErrorMixin, ValueError):
    ...


class ConfigError(RuntimeError):
    ...


class MissingError(PydanticValueError):
    msg_template = ...


class ExtraError(PydanticValueError):
    msg_template = ...


class NoneIsNotAllowedError(PydanticTypeError):
    code = ...
    msg_template = ...


class NoneIsAllowedError(PydanticTypeError):
    code = ...
    msg_template = ...


class WrongConstantError(PydanticValueError):
    code = ...
    def __str__(self) -> str:
        ...
    


class BoolError(PydanticTypeError):
    msg_template = ...


class BytesError(PydanticTypeError):
    msg_template = ...


class DictError(PydanticTypeError):
    msg_template = ...


class EmailError(PydanticValueError):
    msg_template = ...


class UrlError(PydanticValueError):
    code = ...


class UrlSchemeError(UrlError):
    code = ...
    msg_template = ...


class UrlSchemePermittedError(UrlError):
    code = ...
    msg_template = ...
    def __init__(self, allowed_schemes: Set[str]):
        ...
    


class UrlUserInfoError(UrlError):
    code = ...
    msg_template = ...


class UrlHostError(UrlError):
    code = ...
    msg_template = ...


class UrlHostTldError(UrlError):
    code = ...
    msg_template = ...


class UrlExtraError(UrlError):
    code = ...
    msg_template = ...


class EnumError(PydanticTypeError):
    def __str__(self) -> str:
        ...
    


class IntegerError(PydanticTypeError):
    msg_template = ...


class FloatError(PydanticTypeError):
    msg_template = ...


class PathError(PydanticTypeError):
    msg_template = ...


class _PathValueError(PydanticValueError):
    def __init__(self, *, path: Path) -> None:
        ...
    


class PathNotExistsError(_PathValueError):
    code = ...
    msg_template = ...


class PathNotAFileError(_PathValueError):
    code = ...
    msg_template = ...


class PathNotADirectoryError(_PathValueError):
    code = ...
    msg_template = ...


class PyObjectError(PydanticTypeError):
    msg_template = ...


class SequenceError(PydanticTypeError):
    msg_template = ...


class IterableError(PydanticTypeError):
    msg_template = ...


class ListError(PydanticTypeError):
    msg_template = ...


class SetError(PydanticTypeError):
    msg_template = ...


class FrozenSetError(PydanticTypeError):
    msg_template = ...


class TupleError(PydanticTypeError):
    msg_template = ...


class TupleLengthError(PydanticValueError):
    code = ...
    msg_template = ...
    def __init__(self, *, actual_length: int, expected_length: int) -> None:
        ...
    


class ListMinLengthError(PydanticValueError):
    code = ...
    msg_template = ...
    def __init__(self, *, limit_value: int) -> None:
        ...
    


class ListMaxLengthError(PydanticValueError):
    code = ...
    msg_template = ...
    def __init__(self, *, limit_value: int) -> None:
        ...
    


class AnyStrMinLengthError(PydanticValueError):
    code = ...
    msg_template = ...
    def __init__(self, *, limit_value: int) -> None:
        ...
    


class AnyStrMaxLengthError(PydanticValueError):
    code = ...
    msg_template = ...
    def __init__(self, *, limit_value: int) -> None:
        ...
    


class StrError(PydanticTypeError):
    msg_template = ...


class StrRegexError(PydanticValueError):
    code = ...
    msg_template = ...
    def __init__(self, *, pattern: str) -> None:
        ...
    


class _NumberBoundError(PydanticValueError):
    def __init__(self, *, limit_value: Union[int, float, Decimal]) -> None:
        ...
    


class NumberNotGtError(_NumberBoundError):
    code = ...
    msg_template = ...


class NumberNotGeError(_NumberBoundError):
    code = ...
    msg_template = ...


class NumberNotLtError(_NumberBoundError):
    code = ...
    msg_template = ...


class NumberNotLeError(_NumberBoundError):
    code = ...
    msg_template = ...


class NumberNotMultipleError(PydanticValueError):
    code = ...
    msg_template = ...
    def __init__(self, *, multiple_of: Union[int, float, Decimal]) -> None:
        ...
    


class DecimalError(PydanticTypeError):
    msg_template = ...


class DecimalIsNotFiniteError(PydanticValueError):
    code = ...
    msg_template = ...


class DecimalMaxDigitsError(PydanticValueError):
    code = ...
    msg_template = ...
    def __init__(self, *, max_digits: int) -> None:
        ...
    


class DecimalMaxPlacesError(PydanticValueError):
    code = ...
    msg_template = ...
    def __init__(self, *, decimal_places: int) -> None:
        ...
    


class DecimalWholeDigitsError(PydanticValueError):
    code = ...
    msg_template = ...
    def __init__(self, *, whole_digits: int) -> None:
        ...
    


class DateTimeError(PydanticValueError):
    msg_template = ...


class DateError(PydanticValueError):
    msg_template = ...


class TimeError(PydanticValueError):
    msg_template = ...


class DurationError(PydanticValueError):
    msg_template = ...


class HashableError(PydanticTypeError):
    msg_template = ...


class UUIDError(PydanticTypeError):
    msg_template = ...


class UUIDVersionError(PydanticValueError):
    code = ...
    msg_template = ...
    def __init__(self, *, required_version: int) -> None:
        ...
    


class ArbitraryTypeError(PydanticTypeError):
    code = ...
    msg_template = ...
    def __init__(self, *, expected_arbitrary_type: AnyType) -> None:
        ...
    


class ClassError(PydanticTypeError):
    code = ...
    msg_template = ...


class SubclassError(PydanticTypeError):
    code = ...
    msg_template = ...
    def __init__(self, *, expected_class: AnyType) -> None:
        ...
    


class JsonError(PydanticValueError):
    msg_template = ...


class JsonTypeError(PydanticTypeError):
    code = ...
    msg_template = ...


class PatternError(PydanticValueError):
    code = ...
    msg_template = ...


class DataclassTypeError(PydanticTypeError):
    code = ...
    msg_template = ...


class CallableError(PydanticTypeError):
    msg_template = ...


class IPvAnyAddressError(PydanticValueError):
    msg_template = ...


class IPvAnyInterfaceError(PydanticValueError):
    msg_template = ...


class IPvAnyNetworkError(PydanticValueError):
    msg_template = ...


class IPv4AddressError(PydanticValueError):
    msg_template = ...


class IPv6AddressError(PydanticValueError):
    msg_template = ...


class IPv4NetworkError(PydanticValueError):
    msg_template = ...


class IPv6NetworkError(PydanticValueError):
    msg_template = ...


class IPv4InterfaceError(PydanticValueError):
    msg_template = ...


class IPv6InterfaceError(PydanticValueError):
    msg_template = ...


class ColorError(PydanticValueError):
    msg_template = ...


class StrictBoolError(PydanticValueError):
    msg_template = ...


class NotDigitError(PydanticValueError):
    code = ...
    msg_template = ...


class LuhnValidationError(PydanticValueError):
    code = ...
    msg_template = ...


class InvalidLengthForBrand(PydanticValueError):
    code = ...
    msg_template = ...


class InvalidByteSize(PydanticValueError):
    msg_template = ...


class InvalidByteSizeUnit(PydanticValueError):
    msg_template = ...


