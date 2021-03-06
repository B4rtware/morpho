"""
This type stub file was generated by pyright.
"""

from grpc._cython import cygrpc

NoCompression = cygrpc.CompressionAlgorithm.none
Deflate = cygrpc.CompressionAlgorithm.deflate
Gzip = cygrpc.CompressionAlgorithm.gzip
_METADATA_STRING_MAPPING = { NoCompression: 'identity',Deflate: 'deflate',Gzip: 'gzip' }
def _compression_algorithm_to_metadata_value(compression):
    ...

def compression_algorithm_to_metadata(compression):
    ...

def create_channel_option(compression):
    ...

def augment_metadata(metadata, compression):
    ...

__all__ = ("NoCompression", "Deflate", "Gzip")
