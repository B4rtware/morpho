"""
This type stub file was generated by pyright.
"""

import logging
from .decorator import BaseDecorator
from typing import Any, Optional

logger = logging.getLogger('connexion.decorators.response')
class ResponseValidator(BaseDecorator):
    def __init__(self, operation, mimetype, validator: Optional[Any] = ...):
        """
        :type operation: Operation
        :type mimetype: str
        :param validator: Validator class that should be used to validate passed data
                          against API schema. Default is jsonschema.Draft4Validator.
        :type validator: jsonschema.IValidator
        """
        self.operation = ...
        self.mimetype = ...
        self.validator = ...
    
    def validate_response(self, data, status_code, headers, url):
        """
        Validates the Response object based on what has been declared in the specification.
        Ensures the response body matches the declated schema.
        :type data: dict
        :type status_code: int
        :type headers: dict
        :rtype bool | None
        """
        ...
    
    def is_json_schema_compatible(self, response_schema):
        """
        Verify if the specified operation responses are JSON schema
        compatible.

        All operations that specify a JSON schema and have content
        type "application/json" or "text/plain" can be validated using
        json_schema package.

        :type response_schema: dict
        :rtype bool
        """
        ...
    
    def __call__(self, function):
        """
        :type function: types.FunctionType
        :rtype: types.FunctionType
        """
        ...
    
    def __repr__(self):
        """
        :rtype: str
        """
        ...
    

