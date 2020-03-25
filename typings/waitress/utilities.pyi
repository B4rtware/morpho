"""
This type stub file was generated by pyright.
"""

import logging
import re
from .rfc7230 import OBS_TEXT, VCHAR

"""Utility functions
"""
logger = logging.getLogger("waitress")
queue_logger = logging.getLogger("waitress.queue")
def find_double_newline(s):
    """Returns the position just after a double newline in the given string."""
    ...

def concat(*args):
    ...

def join(seq, field=...):
    ...

def group(s):
    ...

short_days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
long_days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
short_day_reg = group(join(short_days, "|"))
long_day_reg = group(join(long_days, "|"))
daymap = {  }
hms_reg = join(3 * [group("[0-9][0-9]")], ":")
months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
monmap = {  }
months_reg = group(join(months, "|"))
rfc822_date = join([concat(short_day_reg, ","), group("[0-9][0-9]?"), months_reg, group("[0-9]+"), hms_reg, "gmt"], " ")
rfc822_reg = re.compile(rfc822_date)
def unpack_rfc822(m):
    ...

rfc850_date = join([concat(long_day_reg, ","), join([group("[0-9][0-9]?"), months_reg, group("[0-9]+")], "-"), hms_reg, "gmt"], " ")
rfc850_reg = re.compile(rfc850_date)
def unpack_rfc850(m):
    ...

weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
monthname = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
def build_http_date(when):
    ...

def parse_http_date(d):
    ...

vchar_re = VCHAR
obs_text_re = OBS_TEXT
qdtext_re = "[\t \x21\x23-\x5b\\\x5d-\x7e" + obs_text_re + "]"
quoted_pair_re = r"\\" + "([\t " + vchar_re + obs_text_re + "])"
quoted_string_re = '"(?:(?:' + qdtext_re + ")|(?:" + quoted_pair_re + '))*"'
quoted_string = re.compile(quoted_string_re)
quoted_pair = re.compile(quoted_pair_re)
def undquote(value):
    ...

def cleanup_unix_socket(path):
    ...

class Error(object):
    code = ...
    reason = ...
    def __init__(self, body):
        self.body = ...
    
    def to_response(self):
        ...
    
    def wsgi_response(self, environ, start_response):
        ...
    


class BadRequest(Error):
    code = ...
    reason = ...


class RequestHeaderFieldsTooLarge(BadRequest):
    code = ...
    reason = ...


class RequestEntityTooLarge(BadRequest):
    code = ...
    reason = ...


class InternalServerError(Error):
    code = ...
    reason = ...


class ServerNotImplemented(Error):
    code = ...
    reason = ...


