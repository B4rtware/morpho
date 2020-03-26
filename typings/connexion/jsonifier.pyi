"""
This type stub file was generated by pyright.
"""

import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        ...
    


class Jsonifier(object):
    """
    Used to serialized and deserialize to/from JSon
    """
    def __init__(self, json_=..., **kwargs):
        """
        :param json_: json library to use. Must have loads() and dumps() method
        :param kwargs: default arguments to pass to json.dumps()
        """
        self.json = ...
        self.dumps_args = ...
    
    def dumps(self, data, **kwargs):
        """ Central point where JSON serialization happens inside
        Connexion.
        """
        ...
    
    def loads(self, data):
        """ Central point where JSON deserialization happens inside
        Connexion.
        """
        ...
    

