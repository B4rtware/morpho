"""
This type stub file was generated by pyright.
"""

import collections
import logging
import grpc

_LOGGER = logging.getLogger(__name__)
class _AuthMetadataContext(collections.namedtuple('AuthMetadataContext', ('service_url', 'method_name')), grpc.AuthMetadataContext):
    ...


class _CallbackState(object):
    def __init__(self):
        self.lock = ...
        self.called = ...
        self.exception = ...
    


class _AuthMetadataPluginCallback(grpc.AuthMetadataPluginCallback):
    def __init__(self, state, callback):
        ...
    
    def __call__(self, metadata, error):
        ...
    


class _Plugin(object):
    def __init__(self, metadata_plugin):
        ...
    
    def __call__(self, service_url, method_name, callback):
        ...
    


def metadata_plugin_call_credentials(metadata_plugin, name):
    ...

