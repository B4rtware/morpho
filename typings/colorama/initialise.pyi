"""
This type stub file was generated by pyright.
"""

import contextlib
from typing import Any, Optional

orig_stdout = None
orig_stderr = None
wrapped_stdout = None
wrapped_stderr = None
atexit_done = False
def reset_all():
    ...

def init(autoreset: bool = ..., convert: Optional[Any] = ..., strip: Optional[Any] = ..., wrap: bool = ...):
    ...

def deinit():
    ...

@contextlib.contextmanager
def colorama_text(*args, **kwargs):
    ...

def reinit():
    ...

def wrap_stream(stream, convert, strip, autoreset, wrap):
    ...

