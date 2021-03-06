"""
This type stub file was generated by pyright.
"""

import socket
import os
from errno import EBADF, ECONNABORTED, ECONNRESET, ENOTCONN, EPIPE, ESHUTDOWN
from typing import Any, Optional

"""Basic infrastructure for asynchronous socket service clients and servers.

There are only two ways to have a program on a single processor do "more
than one thing at a time".  Multi-threaded programming is the simplest and
most popular way to do it, but there is another very different technique,
that lets you have nearly all the advantages of multi-threading, without
actually using multiple threads. it's really only practical if your program
is largely I/O bound. If your program is CPU bound, then pre-emptive
scheduled threads are probably what you really need. Network servers are
rarely CPU-bound, however.

If your operating system supports the select() system call in its I/O
library (and nearly all do), then you can use it to juggle multiple
communication channels at once; doing other work while your I/O is taking
place in the "background."  Although this strategy can seem strange and
complex, especially at first, it is in many ways easier to understand and
control than multi-threaded programming. The module documented here solves
many of the difficult problems for you, making the task of building
sophisticated high-performance network servers and clients a snap.

NB: this is a fork of asyncore from the stdlib that we've (the waitress
developers) named 'wasyncore' to ensure forward compatibility, as asyncore
in the stdlib will be dropped soon.  It is neither a copy of the 2.7 asyncore
nor the 3.X asyncore; it is a version compatible with either 2.7 or 3.X.
"""
_DISCONNECTED = frozenset(ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED, EPIPE, EBADF)
def _strerror(err):
    ...

class ExitNow(Exception):
    ...


_reraised_exceptions = (ExitNow, KeyboardInterrupt, SystemExit)
def read(obj):
    ...

def write(obj):
    ...

def _exception(obj):
    ...

def readwrite(obj, flags):
    ...

def poll(timeout=..., map: Optional[Any] = ...):
    ...

def poll2(timeout=..., map: Optional[Any] = ...):
    ...

poll3 = poll2
def loop(timeout=..., use_poll: bool = ..., map: Optional[Any] = ..., count: Optional[Any] = ...):
    ...

def compact_traceback():
    ...

class dispatcher:
    debug = ...
    connected = ...
    accepting = ...
    connecting = ...
    closing = ...
    addr = ...
    ignore_log_types = ...
    logger = ...
    compact_traceback = ...
    def __init__(self, sock: Optional[Any] = ..., map: Optional[Any] = ...):
        ...
    
    def __repr__(self):
        ...
    
    __str__ = ...
    def add_channel(self, map: Optional[Any] = ...):
        ...
    
    def del_channel(self, map: Optional[Any] = ...):
        ...
    
    def create_socket(self, family=..., type=...):
        self.family_and_type = ...
    
    def set_socket(self, sock, map: Optional[Any] = ...):
        self.socket = ...
    
    def set_reuse_addr(self):
        ...
    
    def readable(self):
        ...
    
    def writable(self):
        ...
    
    def listen(self, num):
        self.accepting = ...
    
    def bind(self, addr):
        self.addr = ...
    
    def connect(self, address):
        self.connected = ...
        self.connecting = ...
    
    def accept(self):
        ...
    
    def send(self, data):
        ...
    
    def recv(self, buffer_size):
        ...
    
    def close(self):
        self.connected = ...
        self.accepting = ...
        self.connecting = ...
    
    def log(self, message):
        ...
    
    def log_info(self, message, type=...):
        ...
    
    def handle_read_event(self):
        ...
    
    def handle_connect_event(self):
        self.connected = ...
        self.connecting = ...
    
    def handle_write_event(self):
        ...
    
    def handle_expt_event(self):
        ...
    
    def handle_error(self):
        ...
    
    def handle_expt(self):
        ...
    
    def handle_read(self):
        ...
    
    def handle_write(self):
        ...
    
    def handle_connect(self):
        ...
    
    def handle_accept(self):
        ...
    
    def handle_accepted(self, sock, addr):
        ...
    
    def handle_close(self):
        ...
    


class dispatcher_with_send(dispatcher):
    def __init__(self, sock: Optional[Any] = ..., map: Optional[Any] = ...):
        self.out_buffer = ...
    
    def initiate_send(self):
        self.out_buffer = ...
    
    handle_write = ...
    def writable(self):
        ...
    
    def send(self, data):
        self.out_buffer = ...
    


def close_all(map: Optional[Any] = ..., ignore_all: bool = ...):
    ...

if os.name == "posix":
    class file_wrapper:
        def __init__(self, fd):
            self.fd = ...
        
        def __del__(self):
            ...
        
        def recv(self, *args):
            ...
        
        def send(self, *args):
            ...
        
        def getsockopt(self, level, optname, buflen: Optional[Any] = ...):
            ...
        
        read = ...
        write = ...
        def close(self):
            self.fd = ...
        
        def fileno(self):
            ...
        
    
    
    class file_dispatcher(dispatcher):
        def __init__(self, fd, map: Optional[Any] = ...):
            self.connected = ...
        
        def set_file(self, fd):
            self.socket = ...
        
    
    
