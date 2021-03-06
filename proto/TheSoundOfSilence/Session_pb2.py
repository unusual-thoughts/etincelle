# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: TheSoundOfSilence/Session.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from TheSoundOfSilence import Picture_pb2 as TheSoundOfSilence_dot_Picture__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='TheSoundOfSilence/Session.proto',
  package='Devialet.AudioSource',
  syntax='proto2',
  serialized_pb=_b('\n\x1fTheSoundOfSilence/Session.proto\x12\x14\x44\x65vialet.AudioSource\x1a\x1fTheSoundOfSilence/Picture.proto\"\x17\n\tSessionId\x12\n\n\x02id\x18\x01 \x02(\x0c\"n\n\x07Session\x12\n\n\x02id\x18\x01 \x02(\x0c\x12\x0c\n\x04name\x18\x02 \x02(\t\x12\x19\n\x11serviceInstanceId\x18\x03 \x02(\t\x12.\n\x07picture\x18\x04 \x02(\x0b\x32\x1d.Devialet.AudioSource.Picture\";\n\x08Sessions\x12/\n\x08sessions\x18\x01 \x03(\x0b\x32\x1d.Devialet.AudioSource.SessionB\x03\x90\x01\x01')
  ,
  dependencies=[TheSoundOfSilence_dot_Picture__pb2.DESCRIPTOR,])




_SESSIONID = _descriptor.Descriptor(
  name='SessionId',
  full_name='Devialet.AudioSource.SessionId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Devialet.AudioSource.SessionId.id', index=0,
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
  serialized_start=90,
  serialized_end=113,
)


_SESSION = _descriptor.Descriptor(
  name='Session',
  full_name='Devialet.AudioSource.Session',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Devialet.AudioSource.Session.id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='Devialet.AudioSource.Session.name', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='serviceInstanceId', full_name='Devialet.AudioSource.Session.serviceInstanceId', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='picture', full_name='Devialet.AudioSource.Session.picture', index=3,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
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
  serialized_start=115,
  serialized_end=225,
)


_SESSIONS = _descriptor.Descriptor(
  name='Sessions',
  full_name='Devialet.AudioSource.Sessions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sessions', full_name='Devialet.AudioSource.Sessions.sessions', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=227,
  serialized_end=286,
)

_SESSION.fields_by_name['picture'].message_type = TheSoundOfSilence_dot_Picture__pb2._PICTURE
_SESSIONS.fields_by_name['sessions'].message_type = _SESSION
DESCRIPTOR.message_types_by_name['SessionId'] = _SESSIONID
DESCRIPTOR.message_types_by_name['Session'] = _SESSION
DESCRIPTOR.message_types_by_name['Sessions'] = _SESSIONS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SessionId = _reflection.GeneratedProtocolMessageType('SessionId', (_message.Message,), dict(
  DESCRIPTOR = _SESSIONID,
  __module__ = 'TheSoundOfSilence.Session_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.AudioSource.SessionId)
  ))
_sym_db.RegisterMessage(SessionId)

Session = _reflection.GeneratedProtocolMessageType('Session', (_message.Message,), dict(
  DESCRIPTOR = _SESSION,
  __module__ = 'TheSoundOfSilence.Session_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.AudioSource.Session)
  ))
_sym_db.RegisterMessage(Session)

Sessions = _reflection.GeneratedProtocolMessageType('Sessions', (_message.Message,), dict(
  DESCRIPTOR = _SESSIONS,
  __module__ = 'TheSoundOfSilence.Session_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.AudioSource.Sessions)
  ))
_sym_db.RegisterMessage(Sessions)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\220\001\001'))
# @@protoc_insertion_point(module_scope)
