# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: TheSoundOfSilence/Track.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from TheSoundOfSilence import Node_pb2 as TheSoundOfSilence_dot_Node__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='TheSoundOfSilence/Track.proto',
  package='Devialet.AudioSource',
  syntax='proto2',
  serialized_pb=_b('\n\x1dTheSoundOfSilence/Track.proto\x12\x14\x44\x65vialet.AudioSource\x1a\x1cTheSoundOfSilence/Node.proto\"\xaf\x01\n\x05Track\x12)\n\x05\x61lbum\x18\x01 \x02(\x0b\x32\x1a.Devialet.AudioSource.Node\x12+\n\x07\x61rtists\x18\x02 \x03(\x0b\x32\x1a.Devialet.AudioSource.Node\x12\x0c\n\x04\x64isc\x18\x03 \x02(\r\x12\x10\n\x08\x64uration\x18\x04 \x02(\r\x12\r\n\x05index\x18\x05 \x02(\r\x12\x10\n\x08readable\x18\x06 \x02(\x08\x12\r\n\x05title\x18\x07 \x02(\t')
  ,
  dependencies=[TheSoundOfSilence_dot_Node__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_TRACK = _descriptor.Descriptor(
  name='Track',
  full_name='Devialet.AudioSource.Track',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='album', full_name='Devialet.AudioSource.Track.album', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='artists', full_name='Devialet.AudioSource.Track.artists', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='disc', full_name='Devialet.AudioSource.Track.disc', index=2,
      number=3, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='duration', full_name='Devialet.AudioSource.Track.duration', index=3,
      number=4, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='index', full_name='Devialet.AudioSource.Track.index', index=4,
      number=5, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='readable', full_name='Devialet.AudioSource.Track.readable', index=5,
      number=6, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='title', full_name='Devialet.AudioSource.Track.title', index=6,
      number=7, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=86,
  serialized_end=261,
)

_TRACK.fields_by_name['album'].message_type = TheSoundOfSilence_dot_Node__pb2._NODE
_TRACK.fields_by_name['artists'].message_type = TheSoundOfSilence_dot_Node__pb2._NODE
DESCRIPTOR.message_types_by_name['Track'] = _TRACK

Track = _reflection.GeneratedProtocolMessageType('Track', (_message.Message,), dict(
  DESCRIPTOR = _TRACK,
  __module__ = 'TheSoundOfSilence.Track_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.AudioSource.Track)
  ))
_sym_db.RegisterMessage(Track)


# @@protoc_insertion_point(module_scope)
