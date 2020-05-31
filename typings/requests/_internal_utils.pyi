"""
This type stub file was generated by pyright.
"""

"""
requests._internal_utils
~~~~~~~~~~~~~~

Provides utility functions that are consumed internally by Requests
which depend on extremely few external helpers (such as compat)
"""
def to_native_string(string, encoding=...):
    """Given a string object, regardless of type, returns a representation of
    that string in the native string type, encoding and decoding where
    necessary. This assumes ASCII unless told otherwise.
    """
    ...

def unicode_is_ascii(u_string):
    """Determine if unicode string only contains ASCII characters.

    :param str u_string: unicode string to check. Must be unicode
        and not Python 2 `str`.
    :rtype: bool
    """
    ...

