# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: TheSoundOfSilence/LiveSource.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from CallMeMaybe import CommonMessages_pb2 as CallMeMaybe_dot_CommonMessages__pb2
from TheSoundOfSilence import Session_pb2 as TheSoundOfSilence_dot_Session__pb2
from TheSoundOfSilence import Picture_pb2 as TheSoundOfSilence_dot_Picture__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='TheSoundOfSilence/LiveSource.proto',
  package='Devialet.AudioSource',
  syntax='proto2',
  serialized_pb=_b('\n\"TheSoundOfSilence/LiveSource.proto\x12\x14\x44\x65vialet.AudioSource\x1a CallMeMaybe/CommonMessages.proto\x1a\x1fTheSoundOfSilence/Session.proto\x1a\x1fTheSoundOfSilence/Picture.proto\"\xc2\x01\n\x0cInputTypeMsg\x12\x0c\n\x04type\x18\x01 \x02(\r\"\xa3\x01\n\tInputType\x12\x12\n\x0eNotDefinedType\x10\x00\x12\n\n\x06TVType\x10\x01\x12\x10\n\x0c\x43\x44PlayerType\x10\x02\x12\x13\n\x0f\x44VDBDPlayerType\x10\x03\x12\x10\n\x0c\x43omputerType\x10\x04\x12\x15\n\x11GamingConsoleType\x10\x05\x12\x13\n\x0fMediaCenterType\x10\x06\x12\x11\n\rTurntableType\x10\x07\"]\n\x12LiveSourceStateMsg\x12\r\n\x05state\x18\x01 \x02(\r\"8\n\x05State\x12\t\n\x05Ready\x10\x01\x12\x0b\n\x07Playing\x10\x02\x12\x0b\n\x07Stopped\x10\x03\x12\n\n\x06Paused\x10\x04\"\x8e\x01\n\x1aLiveSourceAvailableMethods\x12\x16\n\x0ehasInputTypeId\x18\x01 \x02(\x08\x12\x1a\n\x12isNameUserEditable\x18\x02 \x02(\x08\x12\x14\n\x0cisSelectable\x18\x03 \x02(\x08\x12&\n\x18\x61llowToDisableAutoSwitch\x18\x04 \x01(\x08:\x04true\" \n\x10LoadSessionQuery\x12\x0c\n\x04name\x18\x01 \x02(\t\"H\n\x12UnloadSessionQuery\x12\x32\n\tsessionId\x18\x01 \x02(\x0b\x32\x1f.Devialet.AudioSource.SessionId2\xb2\x01\n\x11LiveSourceSession\x12G\n\x07picture\x12\x1b.Devialet.CallMeMaybe.Empty\x1a\x1d.Devialet.AudioSource.Picture\"\x00\x12T\n\rdefaultVolume\x12\x1b.Devialet.CallMeMaybe.Empty\x1a$.Devialet.CallMeMaybe.DoubleProperty\"\x00\x32\xbe\x01\n\nLiveSource\x12V\n\x0bloadSession\x12&.Devialet.AudioSource.LoadSessionQuery\x1a\x1d.Devialet.AudioSource.Session\"\x00\x12X\n\runloadSession\x12(.Devialet.AudioSource.UnloadSessionQuery\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00')
  ,
  dependencies=[CallMeMaybe_dot_CommonMessages__pb2.DESCRIPTOR,TheSoundOfSilence_dot_Session__pb2.DESCRIPTOR,TheSoundOfSilence_dot_Picture__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_INPUTTYPEMSG_INPUTTYPE = _descriptor.EnumDescriptor(
  name='InputType',
  full_name='Devialet.AudioSource.InputTypeMsg.InputType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NotDefinedType', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TVType', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CDPlayerType', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DVDBDPlayerType', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ComputerType', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GamingConsoleType', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MediaCenterType', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TurntableType', index=7, number=7,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=192,
  serialized_end=355,
)
_sym_db.RegisterEnumDescriptor(_INPUTTYPEMSG_INPUTTYPE)

_LIVESOURCESTATEMSG_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='Devialet.AudioSource.LiveSourceStateMsg.State',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Ready', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Playing', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Stopped', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Paused', index=3, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=394,
  serialized_end=450,
)
_sym_db.RegisterEnumDescriptor(_LIVESOURCESTATEMSG_STATE)


_INPUTTYPEMSG = _descriptor.Descriptor(
  name='InputTypeMsg',
  full_name='Devialet.AudioSource.InputTypeMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Devialet.AudioSource.InputTypeMsg.type', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _INPUTTYPEMSG_INPUTTYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=161,
  serialized_end=355,
)


_LIVESOURCESTATEMSG = _descriptor.Descriptor(
  name='LiveSourceStateMsg',
  full_name='Devialet.AudioSource.LiveSourceStateMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='Devialet.AudioSource.LiveSourceStateMsg.state', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _LIVESOURCESTATEMSG_STATE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=357,
  serialized_end=450,
)


_LIVESOURCEAVAILABLEMETHODS = _descriptor.Descriptor(
  name='LiveSourceAvailableMethods',
  full_name='Devialet.AudioSource.LiveSourceAvailableMethods',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='hasInputTypeId', full_name='Devialet.AudioSource.LiveSourceAvailableMethods.hasInputTypeId', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isNameUserEditable', full_name='Devialet.AudioSource.LiveSourceAvailableMethods.isNameUserEditable', index=1,
      number=2, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isSelectable', full_name='Devialet.AudioSource.LiveSourceAvailableMethods.isSelectable', index=2,
      number=3, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='allowToDisableAutoSwitch', full_name='Devialet.AudioSource.LiveSourceAvailableMethods.allowToDisableAutoSwitch', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
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
  serialized_start=453,
  serialized_end=595,
)


_LOADSESSIONQUERY = _descriptor.Descriptor(
  name='LoadSessionQuery',
  full_name='Devialet.AudioSource.LoadSessionQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Devialet.AudioSource.LoadSessionQuery.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  serialized_start=597,
  serialized_end=629,
)


_UNLOADSESSIONQUERY = _descriptor.Descriptor(
  name='UnloadSessionQuery',
  full_name='Devialet.AudioSource.UnloadSessionQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sessionId', full_name='Devialet.AudioSource.UnloadSessionQuery.sessionId', index=0,
      number=1, type=11, cpp_type=10, label=2,
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
  serialized_start=631,
  serialized_end=703,
)

_INPUTTYPEMSG_INPUTTYPE.containing_type = _INPUTTYPEMSG
_LIVESOURCESTATEMSG_STATE.containing_type = _LIVESOURCESTATEMSG
_UNLOADSESSIONQUERY.fields_by_name['sessionId'].message_type = TheSoundOfSilence_dot_Session__pb2._SESSIONID
DESCRIPTOR.message_types_by_name['InputTypeMsg'] = _INPUTTYPEMSG
DESCRIPTOR.message_types_by_name['LiveSourceStateMsg'] = _LIVESOURCESTATEMSG
DESCRIPTOR.message_types_by_name['LiveSourceAvailableMethods'] = _LIVESOURCEAVAILABLEMETHODS
DESCRIPTOR.message_types_by_name['LoadSessionQuery'] = _LOADSESSIONQUERY
DESCRIPTOR.message_types_by_name['UnloadSessionQuery'] = _UNLOADSESSIONQUERY

InputTypeMsg = _reflection.GeneratedProtocolMessageType('InputTypeMsg', (_message.Message,), dict(
  DESCRIPTOR = _INPUTTYPEMSG,
  __module__ = 'TheSoundOfSilence.LiveSource_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.AudioSource.InputTypeMsg)
  ))
_sym_db.RegisterMessage(InputTypeMsg)

LiveSourceStateMsg = _reflection.GeneratedProtocolMessageType('LiveSourceStateMsg', (_message.Message,), dict(
  DESCRIPTOR = _LIVESOURCESTATEMSG,
  __module__ = 'TheSoundOfSilence.LiveSource_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.AudioSource.LiveSourceStateMsg)
  ))
_sym_db.RegisterMessage(LiveSourceStateMsg)

LiveSourceAvailableMethods = _reflection.GeneratedProtocolMessageType('LiveSourceAvailableMethods', (_message.Message,), dict(
  DESCRIPTOR = _LIVESOURCEAVAILABLEMETHODS,
  __module__ = 'TheSoundOfSilence.LiveSource_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.AudioSource.LiveSourceAvailableMethods)
  ))
_sym_db.RegisterMessage(LiveSourceAvailableMethods)

LoadSessionQuery = _reflection.GeneratedProtocolMessageType('LoadSessionQuery', (_message.Message,), dict(
  DESCRIPTOR = _LOADSESSIONQUERY,
  __module__ = 'TheSoundOfSilence.LiveSource_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.AudioSource.LoadSessionQuery)
  ))
_sym_db.RegisterMessage(LoadSessionQuery)

UnloadSessionQuery = _reflection.GeneratedProtocolMessageType('UnloadSessionQuery', (_message.Message,), dict(
  DESCRIPTOR = _UNLOADSESSIONQUERY,
  __module__ = 'TheSoundOfSilence.LiveSource_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.AudioSource.UnloadSessionQuery)
  ))
_sym_db.RegisterMessage(UnloadSessionQuery)


# @@protoc_insertion_point(module_scope)
