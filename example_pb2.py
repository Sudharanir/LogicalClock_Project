# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rexample.proto\"6\n\x06\x45vents\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x11\n\tinterface\x18\x02 \x01(\t\x12\r\n\x05money\x18\x03 \x01(\x05\"=\n\x07Request\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x17\n\x06\x65vents\x18\x02 \x03(\x0b\x32\x07.Events\x12\r\n\x05\x63lock\x18\x03 \x01(\x05\"8\n\rEventExecuted\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05\x63lock\x18\x03 \x01(\x05\"9\n\rClockResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x1c\n\x04\x64\x61ta\x18\x02 \x03(\x0b\x32\x0e.EventExecuted\"8\n\x04Recv\x12\x11\n\tinterface\x18\x01 \x01(\t\x12\x0e\n\x06result\x18\x02 \x01(\t\x12\r\n\x05money\x18\x03 \x01(\x05\"+\n\x08Response\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x13\n\x04recv\x18\x02 \x03(\x0b\x32\x05.Recv28\n\x0bRPCServicer\x12)\n\x0bMsgDelivery\x12\x08.Request\x1a\x0e.ClockResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'example_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EVENTS._serialized_start=17
  _EVENTS._serialized_end=71
  _REQUEST._serialized_start=73
  _REQUEST._serialized_end=134
  _EVENTEXECUTED._serialized_start=136
  _EVENTEXECUTED._serialized_end=192
  _CLOCKRESPONSE._serialized_start=194
  _CLOCKRESPONSE._serialized_end=251
  _RECV._serialized_start=253
  _RECV._serialized_end=309
  _RESPONSE._serialized_start=311
  _RESPONSE._serialized_end=354
  _RPCSERVICER._serialized_start=356
  _RPCSERVICER._serialized_end=412
# @@protoc_insertion_point(module_scope)
