"""
This type stub file was generated by pyright.
"""

import os
from . import wasyncore
from typing import Any, Optional

class _triggerbase(object):
    """OS-independent base class for OS-dependent trigger class."""
    kind = ...
    def __init__(self):
        self.lock = ...
        self.thunks = ...
    
    def readable(self):
        ...
    
    def writable(self):
        ...
    
    def handle_connect(self):
        ...
    
    def handle_close(self):
        ...
    
    def close(self):
        ...
    
    def pull_trigger(self, thunk: Optional[Any] = ...):
        ...
    
    def handle_read(self):
        ...
    


if os.name == "posix":
    class trigger(_triggerbase, wasyncore.file_dispatcher):
        kind = ...
        def __init__(self, map):
            ...
        
        def _close(self):
            ...
        
        def _physical_pull(self):
            ...
        
    
    
else:
    class trigger(_triggerbase, wasyncore.dispatcher):
        kind = ...
        def __init__(self, map):
            self.trigger = ...
        
        def _close(self):
            ...
        
        def _physical_pull(self):
            ...
        
    
    
