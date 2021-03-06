"""
This type stub file was generated by pyright.
"""

import io
import logging
from typing import Any, Optional

"""
    Snippets API

    Test description  # noqa: E501

    OpenAPI spec version: v1
    Contact: contact@snippets.local
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""
logger = logging.getLogger(__name__)
class RESTResponse(io.IOBase):
    def __init__(self, resp):
        self.urllib3_response = ...
        self.status = ...
        self.reason = ...
        self.data = ...
    
    def getheaders(self):
        """Returns a dictionary of the response headers."""
        ...
    
    def getheader(self, name, default: Optional[Any] = ...):
        """Returns a given response header."""
        ...
    


class RESTClientObject(object):
    def __init__(self, configuration, pools_size=..., maxsize: Optional[Any] = ...):
        ...
    
    def request(self, method, url, query_params: Optional[Any] = ..., headers: Optional[Any] = ..., body: Optional[Any] = ..., post_params: Optional[Any] = ..., _preload_content: bool = ..., _request_timeout: Optional[Any] = ...):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param query_params: query parameters in the url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        :param post_params: request post parameters,
                            `application/x-www-form-urlencoded`
                            and `multipart/form-data`
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        """
        ...
    
    def GET(self, url, headers: Optional[Any] = ..., query_params: Optional[Any] = ..., _preload_content: bool = ..., _request_timeout: Optional[Any] = ...):
        ...
    
    def HEAD(self, url, headers: Optional[Any] = ..., query_params: Optional[Any] = ..., _preload_content: bool = ..., _request_timeout: Optional[Any] = ...):
        ...
    
    def OPTIONS(self, url, headers: Optional[Any] = ..., query_params: Optional[Any] = ..., post_params: Optional[Any] = ..., body: Optional[Any] = ..., _preload_content: bool = ..., _request_timeout: Optional[Any] = ...):
        ...
    
    def DELETE(self, url, headers: Optional[Any] = ..., query_params: Optional[Any] = ..., body: Optional[Any] = ..., _preload_content: bool = ..., _request_timeout: Optional[Any] = ...):
        ...
    
    def POST(self, url, headers: Optional[Any] = ..., query_params: Optional[Any] = ..., post_params: Optional[Any] = ..., body: Optional[Any] = ..., _preload_content: bool = ..., _request_timeout: Optional[Any] = ...):
        ...
    
    def PUT(self, url, headers: Optional[Any] = ..., query_params: Optional[Any] = ..., post_params: Optional[Any] = ..., body: Optional[Any] = ..., _preload_content: bool = ..., _request_timeout: Optional[Any] = ...):
        ...
    
    def PATCH(self, url, headers: Optional[Any] = ..., query_params: Optional[Any] = ..., post_params: Optional[Any] = ..., body: Optional[Any] = ..., _preload_content: bool = ..., _request_timeout: Optional[Any] = ...):
        ...
    


class ApiException(Exception):
    def __init__(self, status: Optional[Any] = ..., reason: Optional[Any] = ..., http_resp: Optional[Any] = ...):
        ...
    
    def __str__(self):
        """Custom error messages for exception"""
        ...
    


