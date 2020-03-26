"""
This type stub file was generated by pyright.
"""

from .proxy_headers import PROXY_HEADERS

"""Adjustments are tunable parameters.
"""
truthy = frozenset(("t", "true", "y", "yes", "on", "1"))
KNOWN_PROXY_HEADERS = frozenset(header.lower().replace("_", "-") for header in PROXY_HEADERS)
def asbool(s):
    """ Return the boolean value ``True`` if the case-lowered value of string
    input ``s`` is any of ``t``, ``true``, ``y``, ``on``, or ``1``, otherwise
    return the boolean value ``False``.  If ``s`` is the value ``None``,
    return ``False``.  If ``s`` is already one of the boolean values ``True``
    or ``False``, return it."""
    ...

def asoctal(s):
    """Convert the given octal string to an actual number."""
    ...

def aslist_cronly(value):
    ...

def aslist(value):
    """ Return a list of strings, separating the input based on newlines
    and, if flatten=True (the default), also split on spaces within
    each line."""
    ...

def asset(value):
    ...

def slash_fixed_str(s):
    ...

def str_iftruthy(s):
    ...

def as_socket_list(sockets):
    """Checks if the elements in the list are of type socket and
    removes them if not."""
    ...

class _str_marker(str):
    ...


class _int_marker(int):
    ...


class _bool_marker(object):
    ...


class Adjustments(object):
    """This class contains tunable parameters.
    """
    _params = ...
    _param_map = ...
    host = ...
    port = ...
    listen = ...
    threads = ...
    trusted_proxy = ...
    trusted_proxy_count = ...
    trusted_proxy_headers = ...
    log_untrusted_proxy_headers = ...
    clear_untrusted_proxy_headers = ...
    url_scheme = ...
    url_prefix = ...
    ident = ...
    backlog = ...
    recv_bytes = ...
    send_bytes = ...
    outbuf_overflow = ...
    outbuf_high_watermark = ...
    inbuf_overflow = ...
    connection_limit = ...
    cleanup_interval = ...
    channel_timeout = ...
    log_socket_errors = ...
    max_request_header_size = ...
    max_request_body_size = ...
    expose_tracebacks = ...
    unix_socket = ...
    unix_socket_perms = ...
    socket_options = ...
    asyncore_loop_timeout = ...
    asyncore_use_poll = ...
    ipv4 = ...
    ipv6 = ...
    sockets = ...
    def __init__(self, **kw):
        self.listen = ...
    
    @classmethod
    def parse_args(cls, argv):
        """Pre-parse command line arguments for input into __init__.  Note that
        this does not cast values into adjustment types, it just creates a
        dictionary suitable for passing into __init__, where __init__ does the
        casting.
        """
        ...
    
    @classmethod
    def check_sockets(cls, sockets):
        ...
    

