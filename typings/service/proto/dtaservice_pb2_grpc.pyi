"""
This type stub file was generated by pyright.
"""

from typing import Callable, Any
from grpc import Channel


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
  def TransformDocument(self, request, context):
    """Request to transform a plain text document
    """
    ...
  
  def ListServices(self, request, context):
    ...
  
  def TransformPipe(self, request, context):
    ...
  


def add_DTAServerServicer_to_server(servicer, server):
  ...
