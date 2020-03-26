"""
This type stub file was generated by pyright.
"""

import logging

logger = logging.getLogger('connexion.resolver')
class Resolution(object):
    def __init__(self, function, operation_id):
        """
        Represents the result of operation resolution

        :param function: The endpoint function
        :type function: types.FunctionType
        """
        self.function = ...
        self.operation_id = ...
    


class Resolver(object):
    def __init__(self, function_resolver=...):
        """
        Standard resolver

        :param function_resolver: Function that resolves functions using an operationId
        :type function_resolver: types.FunctionType
        """
        self.function_resolver = ...
    
    def resolve(self, operation):
        """
        Default operation resolver

        :type operation: connexion.operations.AbstractOperation
        """
        ...
    
    def resolve_operation_id(self, operation):
        """
        Default operationId resolver

        :type operation: connexion.operations.AbstractOperation
        """
        ...
    
    def resolve_function_from_operation_id(self, operation_id):
        """
        Invokes the function_resolver

        :type operation_id: str
        """
        ...
    


class RestyResolver(Resolver):
    """
    Resolves endpoint functions using REST semantics (unless overridden by specifying operationId)
    """
    def __init__(self, default_module_name, collection_endpoint_name=...):
        """
        :param default_module_name: Default module name for operations
        :type default_module_name: str
        """
        self.default_module_name = ...
        self.collection_endpoint_name = ...
    
    def resolve_operation_id(self, operation):
        """
        Resolves the operationId using REST semantics unless explicitly configured in the spec

        :type operation: connexion.operations.AbstractOperation
        """
        ...
    
    def resolve_operation_id_using_rest_semantics(self, operation):
        """
        Resolves the operationId using REST semantics

        :type operation: connexion.operations.AbstractOperation
        """
        ...
    


class MethodViewResolver(RestyResolver):
    """
    Resolves endpoint functions based on Flask's MethodView semantics, e.g. ::

            paths:
                /foo_bar:
                    get:
                        # Implied function call: api.FooBarView().get

            class FooBarView(MethodView):
                def get(self):
                    return ...
                def post(self):
                    return ...
    """
    def resolve_operation_id(self, operation):
        """
        Resolves the operationId using REST semantics unless explicitly configured in the spec
        Once resolved with REST semantics the view_name is capitalised and has 'View' added
        to it so it now matches the Class names of the MethodView

        :type operation: connexion.operations.AbstractOperation
        """
        ...
    
    def resolve_function_from_operation_id(self, operation_id):
        """
        Invokes the function_resolver

        :type operation_id: str
        """
        ...
    

