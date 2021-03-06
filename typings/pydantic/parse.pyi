"""
This type stub file was generated by pyright.
"""

import json
import pickle
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Union
from .types import StrBytes

class Protocol(str, Enum):
    json = ...
    pickle = ...


def load_str_bytes(b: StrBytes, *, content_type: str = ..., encoding: str = ..., proto: Protocol = ..., allow_pickle: bool = ..., json_loads: Callable[[str], Any] = ...) -> Any:
    ...

def load_file(path: Union[str, Path], *, content_type: str = ..., encoding: str = ..., proto: Protocol = ..., allow_pickle: bool = ..., json_loads: Callable[[str], Any] = ...) -> Any:
    ...

