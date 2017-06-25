# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: TheSoundOfSilence/TrackDetails.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from TheSoundOfSilence import Track_pb2 as TheSoundOfSilence_dot_Track__pb2
from TheSoundOfSilence import Picture_pb2 as TheSoundOfSilence_dot_Picture__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='TheSoundOfSilence/TrackDetails.proto',
  package='Devialet.AudioSource',
  syntax='proto2',
  serialized_pb=_b('\n$TheSoundOfSilence/TrackDetails.proto\x12\x14\x44\x65vialet.AudioSource\x1a\x1dTheSoundOfSilence/Track.proto\x1a\x1fTheSoundOfSilence/Picture.proto\"\x9e\x01\n\x0cTrackDetails\x12*\n\x05track\x18\x01 \x02(\x0b\x32\x1b.Devialet.AudioSource.Track\x12\x32\n\tpictureId\x18\x02 \x02(\x0b\x32\x1f.Devialet.AudioSource.PictureId\x12.\n\x07picture\x18\x03 \x02(\x0b\x32\x1d.Devialet.AudioSource.Picture\"J\n\rTracksDetails\x12\x39\n\rtracksDetails\x18\x01 \x03(\x0b\x32\".Devialet.AudioSource.TrackDetailsB\x03\x90\x01\x01')
  ,
  dependencies=[TheSoundOfSilence_dot_Track__pb2.DESCRIPTOR,TheSoundOfSilence_dot_Picture__pb2.DESCRIPTOR,])




_TRACKDETAILS = _descriptor.Descriptor(
  name='TrackDetails',
  full_name='Devialet.AudioSource.TrackDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='track', full_name='Devialet.AudioSource.TrackDetails.track', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='pictureId', full_name='Devialet.AudioSource.TrackDetails.pictureId', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='picture', full_name='Devialet.AudioSource.TrackDetails.picture', index=2,
      number=3, type=11, cpp_type=10, label=2,
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
  serialized_start=127,
  serialized_end=285,
)


_TRACKSDETAILS = _descriptor.Descriptor(
  name='TracksDetails',
  full_name='Devialet.AudioSource.TracksDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tracksDetails', full_name='Devialet.AudioSource.TracksDetails.tracksDetails', index=0,
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
  serialized_start=287,
  serialized_end=361,
)

_TRACKDETAILS.fields_by_name['track'].message_type = TheSoundOfSilence_dot_Track__pb2._TRACK
_TRACKDETAILS.fields_by_name['pictureId'].message_type = TheSoundOfSilence_dot_Picture__pb2._PICTUREID
_TRACKDETAILS.fields_by_name['picture'].message_type = TheSoundOfSilence_dot_Picture__pb2._PICTURE
_TRACKSDETAILS.fields_by_name['tracksDetails'].message_type = _TRACKDETAILS
DESCRIPTOR.message_types_by_name['TrackDetails'] = _TRACKDETAILS
DESCRIPTOR.message_types_by_name['TracksDetails'] = _TRACKSDETAILS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TrackDetails = _reflection.GeneratedProtocolMessageType('TrackDetails', (_message.Message,), dict(
  DESCRIPTOR = _TRACKDETAILS,
  __module__ = 'TheSoundOfSilence.TrackDetails_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.AudioSource.TrackDetails)
  ))
_sym_db.RegisterMessage(TrackDetails)

TracksDetails = _reflection.GeneratedProtocolMessageType('TracksDetails', (_message.Message,), dict(
  DESCRIPTOR = _TRACKSDETAILS,
  __module__ = 'TheSoundOfSilence.TrackDetails_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.AudioSource.TracksDetails)
  ))
_sym_db.RegisterMessage(TracksDetails)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\220\001\001'))
# @@protoc_insertion_point(module_scope)