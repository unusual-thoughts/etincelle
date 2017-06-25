# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: TooManyFlows/Identifier.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='TooManyFlows/Identifier.proto',
  package='Devialet.TooManyFlows',
  syntax='proto2',
  serialized_pb=_b('\n\x1dTooManyFlows/Identifier.proto\x12\x15\x44\x65vialet.TooManyFlows\"\x17\n\tBouquetId\x12\n\n\x02id\x18\x01 \x02(\x0c\"\x15\n\x07GroupId\x12\n\n\x02id\x18\x01 \x02(\x0c\"\x16\n\x08PlayerId\x12\n\n\x02id\x18\x01 \x02(\x0c\"\x18\n\nRendererId\x12\n\n\x02id\x18\x01 \x02(\x0c\x42\x03\x90\x01\x01')
)




_BOUQUETID = _descriptor.Descriptor(
  name='BouquetId',
  full_name='Devialet.TooManyFlows.BouquetId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Devialet.TooManyFlows.BouquetId.id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=56,
  serialized_end=79,
)


_GROUPID = _descriptor.Descriptor(
  name='GroupId',
  full_name='Devialet.TooManyFlows.GroupId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Devialet.TooManyFlows.GroupId.id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=81,
  serialized_end=102,
)


_PLAYERID = _descriptor.Descriptor(
  name='PlayerId',
  full_name='Devialet.TooManyFlows.PlayerId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Devialet.TooManyFlows.PlayerId.id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=104,
  serialized_end=126,
)


_RENDERERID = _descriptor.Descriptor(
  name='RendererId',
  full_name='Devialet.TooManyFlows.RendererId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Devialet.TooManyFlows.RendererId.id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=128,
  serialized_end=152,
)

DESCRIPTOR.message_types_by_name['BouquetId'] = _BOUQUETID
DESCRIPTOR.message_types_by_name['GroupId'] = _GROUPID
DESCRIPTOR.message_types_by_name['PlayerId'] = _PLAYERID
DESCRIPTOR.message_types_by_name['RendererId'] = _RENDERERID
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BouquetId = _reflection.GeneratedProtocolMessageType('BouquetId', (_message.Message,), dict(
  DESCRIPTOR = _BOUQUETID,
  __module__ = 'TooManyFlows.Identifier_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.TooManyFlows.BouquetId)
  ))
_sym_db.RegisterMessage(BouquetId)

GroupId = _reflection.GeneratedProtocolMessageType('GroupId', (_message.Message,), dict(
  DESCRIPTOR = _GROUPID,
  __module__ = 'TooManyFlows.Identifier_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.TooManyFlows.GroupId)
  ))
_sym_db.RegisterMessage(GroupId)

PlayerId = _reflection.GeneratedProtocolMessageType('PlayerId', (_message.Message,), dict(
  DESCRIPTOR = _PLAYERID,
  __module__ = 'TooManyFlows.Identifier_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.TooManyFlows.PlayerId)
  ))
_sym_db.RegisterMessage(PlayerId)

RendererId = _reflection.GeneratedProtocolMessageType('RendererId', (_message.Message,), dict(
  DESCRIPTOR = _RENDERERID,
  __module__ = 'TooManyFlows.Identifier_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.TooManyFlows.RendererId)
  ))
_sym_db.RegisterMessage(RendererId)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\220\001\001'))
# @@protoc_insertion_point(module_scope)