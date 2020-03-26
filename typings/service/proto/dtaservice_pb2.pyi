"""
This type stub file was generated by pyright.
"""

import sys
from google.protobuf import descriptor as _descriptor, message as _message, reflection as _reflection, symbol_database as _symbol_database
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2

_b = sys.version_info[0] < 3 and lambda x: x or lambda x: x.encode('latin1')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='dtaservice.proto', package='dtaservice', syntax='proto3', serialized_options=_b('\n\024de.tu-berlin.qds.dtaB\010DTAProtoP\001'), serialized_pb=_b('\n\x10\x64taservice.proto\x12\ndtaservice\x1a\x1cgoogle/api/annotations.proto\"]\n\x0f\x44ocumentRequest\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x10\n\x08\x64ocument\x18\x02 \x01(\x0c\x12\x14\n\x0cservice_name\x18\x03 \x01(\t\x12\x0f\n\x07options\x18\x04 \x03(\t\"X\n\x19TransformDocumentResponse\x12\x16\n\x0etrans_document\x18\x01 \x01(\x0c\x12\x14\n\x0ctrans_output\x18\x02 \x03(\t\x12\r\n\x05\x65rror\x18\x03 \x03(\t\"\x14\n\x12ListServiceRequest\"(\n\x14ListServicesResponse\x12\x10\n\x08services\x18\x01 \x03(\t\"A\n\x14TransformPipeRequest\x12)\n\x04pipe\x18\x01 \x03(\x0b\x32\x1b.dtaservice.DocumentRequest2\x82\x03\n\tDTAServer\x12~\n\x11TransformDocument\x12\x1b.dtaservice.DocumentRequest\x1a%.dtaservice.TransformDocumentResponse\"%\x82\xd3\xe4\x93\x02\x1f\"\x1a/v1/dta/document/transform:\x01*\x12n\n\x0cListServices\x12\x1e.dtaservice.ListServiceRequest\x1a .dtaservice.ListServicesResponse\"\x1c\x82\xd3\xe4\x93\x02\x16\x12\x14/v1/dta/service/list\x12\x84\x01\n\rTransformPipe\x12 .dtaservice.TransformPipeRequest\x1a%.dtaservice.TransformDocumentResponse\"*\x82\xd3\xe4\x93\x02$\"\x1f/v1/dta/document/transform-pipe:\x01*B\"\n\x14\x64\x65.tu-berlin.qds.dtaB\x08\x44TAProtoP\x01\x62\x06proto3'), dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR])
_DOCUMENTREQUEST = _descriptor.Descriptor(name='DocumentRequest', full_name='dtaservice.DocumentRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='file_name', full_name='dtaservice.DocumentRequest.file_name', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b("").decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR), _descriptor.FieldDescriptor(name='document', full_name='dtaservice.DocumentRequest.document', index=1, number=2, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(""), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR), _descriptor.FieldDescriptor(name='service_name', full_name='dtaservice.DocumentRequest.service_name', index=2, number=3, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b("").decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR), _descriptor.FieldDescriptor(name='options', full_name='dtaservice.DocumentRequest.options', index=3, number=4, type=9, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=62, serialized_end=155)
_TRANSFORMDOCUMENTRESPONSE = _descriptor.Descriptor(name='TransformDocumentResponse', full_name='dtaservice.TransformDocumentResponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='trans_document', full_name='dtaservice.TransformDocumentResponse.trans_document', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=_b(""), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR), _descriptor.FieldDescriptor(name='trans_output', full_name='dtaservice.TransformDocumentResponse.trans_output', index=1, number=2, type=9, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR), _descriptor.FieldDescriptor(name='error', full_name='dtaservice.TransformDocumentResponse.error', index=2, number=3, type=9, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=157, serialized_end=245)
_LISTSERVICEREQUEST = _descriptor.Descriptor(name='ListServiceRequest', full_name='dtaservice.ListServiceRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=247, serialized_end=267)
_LISTSERVICESRESPONSE = _descriptor.Descriptor(name='ListServicesResponse', full_name='dtaservice.ListServicesResponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='services', full_name='dtaservice.ListServicesResponse.services', index=0, number=1, type=9, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=269, serialized_end=309)
_TRANSFORMPIPEREQUEST = _descriptor.Descriptor(name='TransformPipeRequest', full_name='dtaservice.TransformPipeRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[_descriptor.FieldDescriptor(name='pipe', full_name='dtaservice.TransformPipeRequest.pipe', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=311, serialized_end=376)
DocumentRequest = _reflection.GeneratedProtocolMessageType('DocumentRequest', (_message.Message, ), { 'DESCRIPTOR': _DOCUMENTREQUEST,'__module__': 'dtaservice_pb2' })
TransformDocumentResponse = _reflection.GeneratedProtocolMessageType('TransformDocumentResponse', (_message.Message, ), { 'DESCRIPTOR': _TRANSFORMDOCUMENTRESPONSE,'__module__': 'dtaservice_pb2' })
ListServiceRequest = _reflection.GeneratedProtocolMessageType('ListServiceRequest', (_message.Message, ), { 'DESCRIPTOR': _LISTSERVICEREQUEST,'__module__': 'dtaservice_pb2' })
ListServicesResponse = _reflection.GeneratedProtocolMessageType('ListServicesResponse', (_message.Message, ), { 'DESCRIPTOR': _LISTSERVICESRESPONSE,'__module__': 'dtaservice_pb2' })
TransformPipeRequest = _reflection.GeneratedProtocolMessageType('TransformPipeRequest', (_message.Message, ), { 'DESCRIPTOR': _TRANSFORMPIPEREQUEST,'__module__': 'dtaservice_pb2' })
_DTASERVER = _descriptor.ServiceDescriptor(name='DTAServer', full_name='dtaservice.DTAServer', file=DESCRIPTOR, index=0, serialized_options=None, serialized_start=379, serialized_end=765, methods=[_descriptor.MethodDescriptor(name='TransformDocument', full_name='dtaservice.DTAServer.TransformDocument', index=0, containing_service=None, input_type=_DOCUMENTREQUEST, output_type=_TRANSFORMDOCUMENTRESPONSE, serialized_options=_b('\202\323\344\223\002\037\"\032/v1/dta/document/transform:\001*')), _descriptor.MethodDescriptor(name='ListServices', full_name='dtaservice.DTAServer.ListServices', index=1, containing_service=None, input_type=_LISTSERVICEREQUEST, output_type=_LISTSERVICESRESPONSE, serialized_options=_b('\202\323\344\223\002\026\022\024/v1/dta/service/list')), _descriptor.MethodDescriptor(name='TransformPipe', full_name='dtaservice.DTAServer.TransformPipe', index=2, containing_service=None, input_type=_TRANSFORMPIPEREQUEST, output_type=_TRANSFORMDOCUMENTRESPONSE, serialized_options=_b('\202\323\344\223\002$\"\037/v1/dta/document/transform-pipe:\001*'))])