# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: format.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x66ormat.proto\x12\x05unary\"\xed\x01\n\x05State\x12\x12\n\ntaskLength\x18\x01 \x01(\x01\x12\x16\n\x0etaskMaxLatency\x18\x02 \x01(\x01\x12\x10\n\x08localCPU\x18\x03 \x01(\x01\x12\x15\n\rlocalMIPSTerm\x18\x04 \x01(\x01\x12\x13\n\x0b\x65\x64geCPUTerm\x18\x05 \x01(\x01\x12\x14\n\x0c\x63loudCPUTerm\x18\x06 \x01(\x01\x12\x13\n\x0bnumberOfPes\x18\x07 \x01(\x01\x12\x10\n\x08\x66ileSize\x18\x08 \x01(\x01\x12\x12\n\noutputSize\x18\t \x01(\x01\x12\x15\n\rcontainerSize\x18\n \x01(\x01\x12\x12\n\nmaxLatency\x18\x0b \x01(\x01\"U\n\x11TrainModelRequest\x12\x1f\n\tnew_state\x18\x01 \x01(\x0b\x32\x0c.unary.State\x12\x0e\n\x06reward\x18\x02 \x01(\x01\x12\x0f\n\x07is_done\x18\x03 \x01(\x08\"\x18\n\x06\x41\x63tion\x12\x0e\n\x06\x61\x63tion\x18\x01 \x01(\x05\"\x1b\n\x08Response\x12\x0f\n\x07message\x18\x01 \x01(\t2r\n\x05Unary\x12,\n\x0bGetActionRL\x12\x0c.unary.State\x1a\r.unary.Action\"\x00\x12;\n\x0cTrainModelRL\x12\x18.unary.TrainModelRequest\x1a\x0f.unary.Response\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'format_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_STATE']._serialized_start=24
  _globals['_STATE']._serialized_end=261
  _globals['_TRAINMODELREQUEST']._serialized_start=263
  _globals['_TRAINMODELREQUEST']._serialized_end=348
  _globals['_ACTION']._serialized_start=350
  _globals['_ACTION']._serialized_end=374
  _globals['_RESPONSE']._serialized_start=376
  _globals['_RESPONSE']._serialized_end=403
  _globals['_UNARY']._serialized_start=405
  _globals['_UNARY']._serialized_end=519
# @@protoc_insertion_point(module_scope)
