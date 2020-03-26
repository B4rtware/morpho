"""
This type stub file was generated by pyright.
"""

import logging
from .decorator import BaseDecorator

logger = logging.getLogger('connexion.decorators.produces')
NoContent = object()
class BaseSerializer(BaseDecorator):
    def __init__(self, mimetype=...):
        """
        :type mimetype: str
        """
        self.mimetype = ...
    
    def __repr__(self):
        """
        :rtype: str
        """
        ...
    


class Produces(BaseSerializer):
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
    

