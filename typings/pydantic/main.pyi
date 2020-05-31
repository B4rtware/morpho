"""
This type stub file was generated by pyright.
"""

import typing_extensions
from abc import ABCMeta
from enum import Enum
from pathlib import Path
from types import FunctionType
from typing import AbstractSet, Any, Callable, Dict, List, Optional, TYPE_CHECKING, Tuple, Type, TypeVar, Union, no_type_check, overload
from .error_wrappers import ValidationError
from .fields import ModelField
from .parse import Protocol
from .types import ModelOrDc, StrBytes
from .typing import AbstractSetIntStr, AnyCallable, CallableGenerator, DictAny, DictStrAny, MappingIntStrAny, ReprArgs, SetStr, TupleGenerator
from .utils import GetterDict, Representation
from inspect import Signature

if TYPE_CHECKING:
    ConfigType = Type['BaseConfig']
    Model = TypeVar('Model', bound='BaseModel')
    class SchemaExtraCallable(typing_extensions.Protocol):
        @overload
        def __call__(self, schema: Dict[str, Any]) -> None:
            ...
        
        @overload
        def __call__(self, schema: Dict[str, Any], model_class: Type[Model]) -> None:
            ...
        
    
    
__all__ = ('BaseConfig', 'BaseModel', 'Extra', 'compiled', 'create_model', 'validate_model')
class Extra(str, Enum):
    allow = ...
    ignore = ...
    forbid = ...


class BaseConfig:
    title = ...
    anystr_strip_whitespace = ...
    min_anystr_length = ...
    max_anystr_length = ...
    validate_all = ...
    extra = ...
    allow_mutation = ...
    allow_population_by_field_name = ...
    use_enum_values = ...
    validate_assignment = ...
    arbitrary_types_allowed = ...
    @classmethod
    def get_field_info(cls, name: str) -> Dict[str, Any]:
        ...
    
    @classmethod
    def prepare_field(cls, field: ModelField) -> None:
        """
        Optional hook to check or modify fields during model creation.
        """
        ...
    


def inherit_config(self_config: ConfigType, parent_config: ConfigType) -> ConfigType:
    ...

EXTRA_LINK = 'https://pydantic-docs.helpmanual.io/usage/model_config/'
def prepare_config(config: Type[BaseConfig], cls_name: str) -> None:
    ...

def is_valid_field(name: str) -> bool:
    ...

def validate_custom_root_type(fields: Dict[str, ModelField]) -> None:
    ...

UNTOUCHED_TYPES = (FunctionType, property, type, classmethod, staticmethod)
_is_base_model_class_defined = False
class ModelMetaclass(ABCMeta):
    @no_type_check
    def __new__(mcs, name, bases, namespace, **kwargs):
        ...
    


class BaseModel(Representation, metaclass=ModelMetaclass):
    if TYPE_CHECKING:
        __pre_root_validators__: List[AnyCallable]
        __post_root_validators__: List[Tuple[bool, AnyCallable]]
        __signature__: Signature
        ...
    Config = ...
    __slots__ = ...
    __doc__ = ...
    def __init__(__pydantic_self__, **data: Any) -> None:
        """
        Create a new model by parsing and validating input data from keyword arguments.

        Raises ValidationError if the input data cannot be parsed to form a valid model.
        """
        ...
    
    @no_type_check
    def __setattr__(self, name, value):
        ...
    
    def __getstate__(self) -> DictAny:
        ...
    
    def __setstate__(self, state: DictAny) -> None:
        ...
    
    def dict(self, *, include: Union[AbstractSetIntStr, MappingIntStrAny] = ..., exclude: Union[AbstractSetIntStr, MappingIntStrAny] = ..., by_alias: bool = ..., skip_defaults: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ...) -> DictStrAny:
        """
        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

        """
        ...
    
    def json(self, *, include: Union[AbstractSetIntStr, MappingIntStrAny] = ..., exclude: Union[AbstractSetIntStr, MappingIntStrAny] = ..., by_alias: bool = ..., skip_defaults: bool = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ..., encoder: Optional[Callable[[Any], Any]] = ..., **dumps_kwargs: Any) -> str:
        """
        Generate a JSON representation of the model, `include` and `exclude` arguments as per `dict()`.

        `encoder` is an optional function to supply as `default` to json.dumps(), other arguments as per `json.dumps()`.
        """
        ...
    
    @classmethod
    def parse_obj(cls: Type[Model], obj: Any) -> Model:
        ...
    
    @classmethod
    def parse_raw(cls: Type[Model], b: StrBytes, *, content_type: str = ..., encoding: str = ..., proto: Protocol = ..., allow_pickle: bool = ...) -> Model:
        ...
    
    @classmethod
    def parse_file(cls: Type[Model], path: Union[str, Path], *, content_type: str = ..., encoding: str = ..., proto: Protocol = ..., allow_pickle: bool = ...) -> Model:
        ...
    
    @classmethod
    def from_orm(cls: Type[Model], obj: Any) -> Model:
        ...
    
    @classmethod
    def construct(cls: Type[Model], _fields_set: Optional[SetStr] = ..., **values: Any) -> Model:
        """
        Creates a new model setting __dict__ and __fields_set__ from trusted or pre-validated data.
        Default values are respected, but no other validation is performed.
        """
        ...
    
    def copy(self: Model, *, include: Union[AbstractSetIntStr, MappingIntStrAny] = ..., exclude: Union[AbstractSetIntStr, MappingIntStrAny] = ..., update: DictStrAny = ..., deep: bool = ...) -> Model:
        """
        Duplicate a model, optionally choose which fields to include, exclude and change.

        :param include: fields to include in new model
        :param exclude: fields to exclude from new model, as with values this takes precedence over include
        :param update: values to change/add in the new model. Note: the data is not validated before creating
            the new model: you should trust this data
        :param deep: set to `True` to make a deep copy of the model
        :return: new model instance
        """
        ...
    
    @classmethod
    def schema(cls, by_alias: bool = ...) -> DictStrAny:
        ...
    
    @classmethod
    def schema_json(cls, *, by_alias: bool = ..., **dumps_kwargs: Any) -> str:
        ...
    
    @classmethod
    def __get_validators__(cls) -> CallableGenerator:
        ...
    
    @classmethod
    def validate(cls: Type[Model], value: Any) -> Model:
        ...
    
    @classmethod
    def _decompose_class(cls: Type[Model], obj: Any) -> GetterDict:
        ...
    
    @classmethod
    @no_type_check
    def _get_value(cls, v: Any, to_dict: bool, by_alias: bool, include: Optional[Union[AbstractSetIntStr, MappingIntStrAny]], exclude: Optional[Union[AbstractSetIntStr, MappingIntStrAny]], exclude_unset: bool, exclude_defaults: bool, exclude_none: bool) -> Any:
        ...
    
    @classmethod
    def update_forward_refs(cls, **localns: Any) -> None:
        """
        Try to update ForwardRefs on fields based on this Model, globalns and localns.
        """
        ...
    
    def __iter__(self) -> TupleGenerator:
        """
        so `dict(model)` works
        """
        ...
    
    def _iter(self, to_dict: bool = ..., by_alias: bool = ..., include: Union[AbstractSetIntStr, MappingIntStrAny] = ..., exclude: Union[AbstractSetIntStr, MappingIntStrAny] = ..., exclude_unset: bool = ..., exclude_defaults: bool = ..., exclude_none: bool = ...) -> TupleGenerator:
        ...
    
    def _calculate_keys(self, include: Optional[Union[AbstractSetIntStr, MappingIntStrAny]], exclude: Optional[Union[AbstractSetIntStr, MappingIntStrAny]], exclude_unset: bool, update: Optional[DictStrAny] = ...) -> Optional[AbstractSet[str]]:
        ...
    
    def __eq__(self, other: Any) -> bool:
        ...
    
    def __repr_args__(self) -> ReprArgs:
        ...
    
    @property
    def fields(self) -> Dict[str, ModelField]:
        ...
    
    def to_string(self, pretty: bool = ...) -> str:
        ...
    
    @property
    def __values__(self) -> DictStrAny:
        ...
    


_is_base_model_class_defined = True
def create_model(__model_name: str, *, __config__: Type[BaseConfig] = ..., __base__: Type[BaseModel] = ..., __module__: Optional[str] = ..., __validators__: Dict[str, classmethod] = ..., **field_definitions: Any) -> Type[BaseModel]:
    """
    Dynamically create a model.
    :param __model_name: name of the created model
    :param __config__: config class to use for the new model
    :param __base__: base class for the new model to inherit from
    :param __validators__: a dict of method names and @validator class methods
    :param **field_definitions: fields of the model (or extra fields if a base is supplied) in the format
        `<name>=(<type>, <default default>)` or `<name>=<default value> eg. `foobar=(str, ...)` or `foobar=123`
    """
    ...

_missing = object()
def validate_model(model: Type[BaseModel], input_data: DictStrAny, cls: ModelOrDc = ...) -> Tuple[DictStrAny, SetStr, Optional[ValidationError]]:
    """
    validate data against a model.
    """
    ...

