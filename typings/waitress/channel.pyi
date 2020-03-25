"""
This type stub file was generated by pyright.
"""

from . import wasyncore
from typing import Any, Optional

class ClientDisconnected(Exception):
    """ Raised when attempting to write to a closed socket."""
    ...


class HTTPChannel(wasyncore.dispatcher, object):
    """
    Setting self.requests = [somerequest] prevents more requests from being
    received until the out buffers have been flushed.

    Setting self.requests = [] allows more requests to be received.
    """
    task_class = ...
    error_task_class = ...
    parser_class = ...
    request = ...
    last_activity = ...
    will_close = ...
    close_when_flushed = ...
    requests = ...
    sent_continue = ...
    total_outbufs_len = ...
    current_outbuf_count = ...
    def __init__(self, server, sock, addr, adj, map: Optional[Any] = ...):
        self.server = ...
        self.adj = ...
        self.outbufs = ...
        self.creation_time = ...
        self.sendbuf_len = ...
        self.task_lock = ...
        self.outbuf_lock = ...
        self.addr = ...
    
    def writable(self):
        ...
    
    def handle_write(self):
        ...
    
    def readable(self):
        ...
    
    def handle_read(self):
        ...
    
    def received(self, data):
        """
        Receives input asynchronously and assigns one or more requests to the
        channel.
        """
        ...
    
    def _flush_some_if_lockable(self):
        ...
    
    def _flush_some(self):
        ...
    
    def handle_close(self):
        ...
    
    def add_channel(self, map: Optional[Any] = ...):
        """See wasyncore.dispatcher

        This hook keeps track of opened channels.
        """
        ...
    
    def del_channel(self, map: Optional[Any] = ...):
        """See wasyncore.dispatcher

        This hook keeps track of closed channels.
        """
        ...
    
    def write_soon(self, data):
        ...
    
    def _flush_outbufs_below_high_watermark(self):
        ...
    
    def service(self):
        """Execute all pending requests """
        self.last_activity = ...
    
    def cancel(self):
        """ Cancels all pending / active requests """
        self.will_close = ...
        self.connected = ...
        self.last_activity = ...
        self.requests = ...
    


