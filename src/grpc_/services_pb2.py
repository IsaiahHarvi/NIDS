# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: src/grpc_/services.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'src/grpc_/services.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18src/grpc_/services.proto\x12\x08services\"P\n\x10\x43omponentMessage\x12\r\n\x05input\x18\x01 \x03(\x02\x12\x14\n\x0chealth_check\x18\x02 \x01(\x08\x12\x17\n\x0f\x63ollection_name\x18\x03 \x01(\t\"7\n\x11\x43omponentResponse\x12\x0e\n\x06output\x18\x01 \x03(\x02\x12\x12\n\nprediction\x18\x02 \x01(\x05\x32O\n\tComponent\x12\x42\n\x07\x66orward\x12\x1a.services.ComponentMessage\x1a\x1b.services.ComponentResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'src.grpc_.services_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_COMPONENTMESSAGE']._serialized_start=38
  _globals['_COMPONENTMESSAGE']._serialized_end=118
  _globals['_COMPONENTRESPONSE']._serialized_start=120
  _globals['_COMPONENTRESPONSE']._serialized_end=175
  _globals['_COMPONENT']._serialized_start=177
  _globals['_COMPONENT']._serialized_end=256
# @@protoc_insertion_point(module_scope)
