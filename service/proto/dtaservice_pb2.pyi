# -----------------------------------------------------------------------------------------------------------------------------
#                                                    Copied Typings
# -----------------------------------------------------------------------------------------------------------------------------

from service.proto.dtaservice_pb2 import ListServiceRequest
from typing import List


class DocumentRequest(_message.Message):
  file_name: str
  service_name: str
  document: bytes
  def __init__(self, document: bytes, file_name: str, service_name: str):
    pass

  # TODO: workaround for dynamically added methods from protobuf.internal.python_message.py
  @staticmethod
  def FromString(cls, s: str) -> DocumentRequest:
    pass


class TransformDocumentResponse(_message.Message):
  trans_document: bytes
  trans_output: List[str]
  error: str
  def __init__(self, trans_document: bytes, trans_output: List[str], error: Optional[str]) -> None:
    pass

  # TODO: workaround for dynamically added methods from protobuf.internal.python_message.py
  @staticmethod
  def FromString(cls, s: str) -> TransformDocumentResponse:
    pass

class ListServiceRequest(_message.Message):
  pass

class ListServicesResponse(_message.Message):
  pass