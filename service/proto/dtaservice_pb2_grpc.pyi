from service.proto.dtaservice_pb2 import ListServicesResponse
from service.proto.dtaservice_pb2 import TransformDocumentResponse
from service.proto.dtaservice_pb2 import TransformPipeRequest
from service.proto.dtaservice_pb2 import ListServiceRequest
from typing import Callable, Any
from grpc import Channel

from service.proto.dtaservice_pb2 import DocumentRequest
from grpc import ServicerContext


class DTAServerStub(object):
  """The DTA service definition.
  """
  def __init__(self, channel: Channel) -> None:
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.TransformDocument: Callable[..., Any]
    self.ListServices = ...
    self.TransformPipe = ...
  


class DTAServerServicer(object):
  """The DTA service definition.
  """
  def TransformDocument(self, request: DocumentRequest, context: ServicerContext) -> TransformDocumentResponse:
    """Request to transform a plain text document
    """
    ...
  
  def ListServices(self, request: ListServiceRequest, context: ServicerContext) -> ListServicesResponse: ...
  def TransformPipe(self, request: TransformPipeRequest, context: ServicerContext): ...
  


def add_DTAServerServicer_to_server(servicer: DTAServerServicer, server):
  ...