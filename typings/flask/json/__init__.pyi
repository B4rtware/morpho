"""
This type stub file was generated by pyright.
"""

import codecs
import io
import uuid
from datetime import date, datetime
from itsdangerous import json as _json
from jinja2 import Markup
from werkzeug.http import http_date
from .._compat import PY2, text_type
from ..globals import current_app, request
from typing import Any, Optional

"""
flask.json
~~~~~~~~~~

:copyright: 2010 Pallets
:license: BSD-3-Clause
"""
_slash_escape = "\\/" not in _json.dumps("/")
__all__ = ["dump", "dumps", "load", "loads", "htmlsafe_dump", "htmlsafe_dumps", "JSONDecoder", "JSONEncoder", "jsonify"]
def _wrap_reader_for_text(fp, encoding):
    ...

def _wrap_writer_for_text(fp, encoding):
    ...

class JSONEncoder(_json.JSONEncoder):
    """The default Flask JSON encoder. This one extends the default
    encoder by also supporting ``datetime``, ``UUID``, ``dataclasses``,
    and ``Markup`` objects.

    ``datetime`` objects are serialized as RFC 822 datetime strings.
    This is the same as the HTTP date format.

    In order to support more data types, override the :meth:`default`
    method.
    """
    def default(self, o):
        """Implement this method in a subclass such that it returns a
        serializable object for ``o``, or calls the base implementation (to
        raise a :exc:`TypeError`).

        For example, to support arbitrary iterators, you could implement
        default like this::

            def default(self, o):
                try:
                    iterable = iter(o)
                except TypeError:
                    pass
                else:
                    return list(iterable)
                return JSONEncoder.default(self, o)
        """
        ...
    


class JSONDecoder(_json.JSONDecoder):
    """The default JSON decoder.  This one does not change the behavior from
    the default simplejson decoder.  Consult the :mod:`json` documentation
    for more information.  This decoder is not only used for the load
    functions of this module but also :attr:`~flask.Request`.
    """
    ...


def _dump_arg_defaults(kwargs, app: Optional[Any] = ...):
    """Inject default arguments for dump functions."""
    ...

def _load_arg_defaults(kwargs, app: Optional[Any] = ...):
    """Inject default arguments for load functions."""
    ...

def detect_encoding(data):
    """Detect which UTF codec was used to encode the given bytes.

    The latest JSON standard (:rfc:`8259`) suggests that only UTF-8 is
    accepted. Older documents allowed 8, 16, or 32. 16 and 32 can be big
    or little endian. Some editors or libraries may prepend a BOM.

    :param data: Bytes in unknown UTF encoding.
    :return: UTF encoding name
    """
    ...

def dumps(obj, app: Optional[Any] = ..., **kwargs):
    """Serialize ``obj`` to a JSON-formatted string. If there is an
    app context pushed, use the current app's configured encoder
    (:attr:`~flask.Flask.json_encoder`), or fall back to the default
    :class:`JSONEncoder`.

    Takes the same arguments as the built-in :func:`json.dumps`, and
    does some extra configuration based on the application. If the
    simplejson package is installed, it is preferred.

    :param obj: Object to serialize to JSON.
    :param app: App instance to use to configure the JSON encoder.
        Uses ``current_app`` if not given, and falls back to the default
        encoder when not in an app context.
    :param kwargs: Extra arguments passed to :func:`json.dumps`.

    .. versionchanged:: 1.0.3

        ``app`` can be passed directly, rather than requiring an app
        context for configuration.
    """
    ...

def dump(obj, fp, app: Optional[Any] = ..., **kwargs):
    """Like :func:`dumps` but writes into a file object."""
    ...

def loads(s, app: Optional[Any] = ..., **kwargs):
    """Deserialize an object from a JSON-formatted string ``s``. If
    there is an app context pushed, use the current app's configured
    decoder (:attr:`~flask.Flask.json_decoder`), or fall back to the
    default :class:`JSONDecoder`.

    Takes the same arguments as the built-in :func:`json.loads`, and
    does some extra configuration based on the application. If the
    simplejson package is installed, it is preferred.

    :param s: JSON string to deserialize.
    :param app: App instance to use to configure the JSON decoder.
        Uses ``current_app`` if not given, and falls back to the default
        encoder when not in an app context.
    :param kwargs: Extra arguments passed to :func:`json.dumps`.

    .. versionchanged:: 1.0.3

        ``app`` can be passed directly, rather than requiring an app
        context for configuration.
    """
    ...

def load(fp, app: Optional[Any] = ..., **kwargs):
    """Like :func:`loads` but reads from a file object."""
    ...

def htmlsafe_dumps(obj, **kwargs):
    """Works exactly like :func:`dumps` but is safe for use in ``<script>``
    tags.  It accepts the same arguments and returns a JSON string.  Note that
    this is available in templates through the ``|tojson`` filter which will
    also mark the result as safe.  Due to how this function escapes certain
    characters this is safe even if used outside of ``<script>`` tags.

    The following characters are escaped in strings:

    -   ``<``
    -   ``>``
    -   ``&``
    -   ``'``

    This makes it safe to embed such strings in any place in HTML with the
    notable exception of double quoted attributes.  In that case single
    quote your attributes or HTML escape it in addition.

    .. versionchanged:: 0.10
       This function's return value is now always safe for HTML usage, even
       if outside of script tags or if used in XHTML.  This rule does not
       hold true when using this function in HTML attributes that are double
       quoted.  Always single quote attributes if you use the ``|tojson``
       filter.  Alternatively use ``|tojson|forceescape``.
    """
    ...

def htmlsafe_dump(obj, fp, **kwargs):
    """Like :func:`htmlsafe_dumps` but writes into a file object."""
    ...

def jsonify(*args, **kwargs):
    """This function wraps :func:`dumps` to add a few enhancements that make
    life easier.  It turns the JSON output into a :class:`~flask.Response`
    object with the :mimetype:`application/json` mimetype.  For convenience, it
    also converts multiple arguments into an array or multiple keyword arguments
    into a dict.  This means that both ``jsonify(1,2,3)`` and
    ``jsonify([1,2,3])`` serialize to ``[1,2,3]``.

    For clarity, the JSON serialization behavior has the following differences
    from :func:`dumps`:

    1. Single argument: Passed straight through to :func:`dumps`.
    2. Multiple arguments: Converted to an array before being passed to
       :func:`dumps`.
    3. Multiple keyword arguments: Converted to a dict before being passed to
       :func:`dumps`.
    4. Both args and kwargs: Behavior undefined and will throw an exception.

    Example usage::

        from flask import jsonify

        @app.route('/_get_current_user')
        def get_current_user():
            return jsonify(username=g.user.username,
                           email=g.user.email,
                           id=g.user.id)

    This will send a JSON response like this to the browser::

        {
            "username": "admin",
            "email": "admin@localhost",
            "id": 42
        }


    .. versionchanged:: 0.11
       Added support for serializing top-level arrays. This introduces a
       security risk in ancient browsers. See :ref:`json-security` for details.

    This function's response will be pretty printed if the
    ``JSONIFY_PRETTYPRINT_REGULAR`` config parameter is set to True or the
    Flask app is running in debug mode. Compressed (not pretty) formatting
    currently means no indents and no spaces after separators.

    .. versionadded:: 0.2
    """
    ...

def tojson_filter(obj, **kwargs):
    ...

