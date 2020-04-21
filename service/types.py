from enum import Enum


# must resides here because otherwise circular import
class ServiceType(Enum):
    SERVICE = ("service",)
    PROXY = ("proxy",)
    GATEWAY = "gateway"