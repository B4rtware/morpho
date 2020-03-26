"""
This type stub file was generated by pyright.
"""

from typing import Any, Optional

"""Buffers
"""
COPY_BYTES = 1 << 18
STRBUF_LIMIT = 8192
class FileBasedBuffer(object):
    remain = ...
    def __init__(self, file, from_buffer: Optional[Any] = ...):
        self.file = ...
    
    def __len__(self):
        ...
    
    def __nonzero__(self):
        ...
    
    __bool__ = ...
    def append(self, s):
        self.remain = ...
    
    def get(self, numbytes=..., skip: bool = ...):
        ...
    
    def skip(self, numbytes, allow_prune=...):
        self.remain = ...
    
    def newfile(self):
        ...
    
    def prune(self):
        self.file = ...
    
    def getfile(self):
        ...
    
    def close(self):
        self.remain = ...
    


class TempfileBasedBuffer(FileBasedBuffer):
    def __init__(self, from_buffer: Optional[Any] = ...):
        ...
    
    def newfile(self):
        ...
    


class BytesIOBasedBuffer(FileBasedBuffer):
    def __init__(self, from_buffer: Optional[Any] = ...):
        ...
    
    def newfile(self):
        ...
    


def _is_seekable(fp):
    ...

class ReadOnlyFileBasedBuffer(FileBasedBuffer):
    def __init__(self, file, block_size=...):
        self.file = ...
        self.block_size = ...
    
    def prepare(self, size: Optional[Any] = ...):
        ...
    
    def get(self, numbytes=..., skip: bool = ...):
        ...
    
    def __iter__(self):
        ...
    
    def next(self):
        ...
    
    __next__ = ...
    def append(self, s):
        ...
    


class OverflowableBuffer(object):
    """
    This buffer implementation has four stages:
    - No data
    - Bytes-based buffer
    - BytesIO-based buffer
    - Temporary file storage
    The first two stages are fastest for simple transfers.
    """
    overflowed = ...
    buf = ...
    strbuf = ...
    def __init__(self, overflow):
        self.overflow = ...
    
    def __len__(self):
        ...
    
    def __nonzero__(self):
        ...
    
    __bool__ = ...
    def _create_buffer(self):
        ...
    
    def _set_small_buffer(self):
        self.buf = ...
        self.overflowed = ...
    
    def _set_large_buffer(self):
        self.buf = ...
        self.overflowed = ...
    
    def append(self, s):
        ...
    
    def get(self, numbytes=..., skip: bool = ...):
        ...
    
    def skip(self, numbytes, allow_prune: bool = ...):
        ...
    
    def prune(self):
        """
        A potentially expensive operation that removes all data
        already retrieved from the buffer.
        """
        ...
    
    def getfile(self):
        ...
    
    def close(self):
        ...
    

