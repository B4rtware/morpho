"""
This type stub file was generated by pyright.
"""

import logging
from typing import Dict, Any
from waitress.server import create_server

def serve(app: object, **kw: Dict[str, Any]) -> None: ...

def serve_paste(app, global_conf, **kw):
    ...

def profile(cmd, globals, locals, sort_order, callers):
    ...

