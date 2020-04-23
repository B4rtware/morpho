from enum import Enum


# must resides here because otherwise circular import
class ServiceType(Enum):
    """Type for a Service"""
    SERVICE = "service"
    PROXY = "proxy"
    GATEWAY = "gateway"