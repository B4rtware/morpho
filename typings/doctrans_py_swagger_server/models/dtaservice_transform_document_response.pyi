"""
This type stub file was generated by pyright.
"""

from typing import List
from doctrans_py_swagger_server.models.base_model_ import Model

class DtaserviceTransformDocumentResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, trans_document: str = ..., trans_output: List[str] = ..., error: List[str] = ...):
        """DtaserviceTransformDocumentResponse - a model defined in Swagger

        :param trans_document: The trans_document of this DtaserviceTransformDocumentResponse.  # noqa: E501
        :type trans_document: str
        :param trans_output: The trans_output of this DtaserviceTransformDocumentResponse.  # noqa: E501
        :type trans_output: List[str]
        :param error: The error of this DtaserviceTransformDocumentResponse.  # noqa: E501
        :type error: List[str]
        """
        self.swagger_types = ...
        self.attribute_map = ...
    
    @classmethod
    def from_dict(cls, dikt) -> DtaserviceTransformDocumentResponse:
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The dtaserviceTransformDocumentResponse of this DtaserviceTransformDocumentResponse.  # noqa: E501
        :rtype: DtaserviceTransformDocumentResponse
        """
        ...
    
    @property
    def trans_document(self) -> str:
        """Gets the trans_document of this DtaserviceTransformDocumentResponse.


        :return: The trans_document of this DtaserviceTransformDocumentResponse.
        :rtype: str
        """
        ...
    
    @trans_document.setter
    def trans_document(self, trans_document: str):
        """Sets the trans_document of this DtaserviceTransformDocumentResponse.


        :param trans_document: The trans_document of this DtaserviceTransformDocumentResponse.
        :type trans_document: str
        """
        ...
    
    @property
    def trans_output(self) -> List[str]:
        """Gets the trans_output of this DtaserviceTransformDocumentResponse.


        :return: The trans_output of this DtaserviceTransformDocumentResponse.
        :rtype: List[str]
        """
        ...
    
    @trans_output.setter
    def trans_output(self, trans_output: List[str]):
        """Sets the trans_output of this DtaserviceTransformDocumentResponse.


        :param trans_output: The trans_output of this DtaserviceTransformDocumentResponse.
        :type trans_output: List[str]
        """
        ...
    
    @property
    def error(self) -> List[str]:
        """Gets the error of this DtaserviceTransformDocumentResponse.


        :return: The error of this DtaserviceTransformDocumentResponse.
        :rtype: List[str]
        """
        ...
    
    @error.setter
    def error(self, error: List[str]):
        """Sets the error of this DtaserviceTransformDocumentResponse.


        :param error: The error of this DtaserviceTransformDocumentResponse.
        :type error: List[str]
        """
        ...
    


