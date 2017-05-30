# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: MasterOfPuppets/Configuration.proto

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


DESCRIPTOR = _descriptor.FileDescriptor(
  name='MasterOfPuppets/Configuration.proto',
  package='Devialet.MasterOfPuppets',
  syntax='proto2',
  serialized_pb=_b('\n#MasterOfPuppets/Configuration.proto\x12\x18\x44\x65vialet.MasterOfPuppets\x1a CallMeMaybe/CommonMessages.proto\"\x15\n\x07GroupId\x12\n\n\x02id\x18\x01 \x02(\x0c\"\x17\n\tBouquetId\x12\n\n\x02id\x18\x01 \x02(\x0c\"\x18\n\nRendererId\x12\n\n\x02id\x18\x01 \x02(\x0c\"k\n\x0cNodeRenderer\x12\x38\n\nrendererId\x18\x01 \x02(\x0b\x32$.Devialet.MasterOfPuppets.RendererId\x12\x0c\n\x04name\x18\x02 \x02(\t\x12\x13\n\x0bisActivated\x18\x03 \x02(\x08\"\x88\x01\n\tNodeGroup\x12\x32\n\x07groupId\x18\x01 \x02(\x0b\x32!.Devialet.MasterOfPuppets.GroupId\x12\x0c\n\x04name\x18\x02 \x02(\t\x12\x39\n\trenderers\x18\x03 \x03(\x0b\x32&.Devialet.MasterOfPuppets.NodeRenderer\"z\n\x0bNodeBouquet\x12\x36\n\tbouquetId\x18\x01 \x02(\x0b\x32#.Devialet.MasterOfPuppets.BouquetId\x12\x33\n\x06groups\x18\x02 \x03(\x0b\x32#.Devialet.MasterOfPuppets.NodeGroup\"C\n\x08NodeRoot\x12\x37\n\x08\x62ouquets\x18\x01 \x03(\x0b\x32%.Devialet.MasterOfPuppets.NodeBouquet\"U\n\rAddGroupQuery\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x36\n\tbouquetId\x18\x02 \x02(\x0b\x32#.Devialet.MasterOfPuppets.BouquetId\"\x8e\x01\n\x10\x41\x64\x64RendererQuery\x12\x38\n\nrendererId\x18\x01 \x02(\x0b\x32$.Devialet.MasterOfPuppets.RendererId\x12\x0c\n\x04name\x18\x02 \x02(\t\x12\x32\n\x07groupId\x18\x03 \x02(\x0b\x32!.Devialet.MasterOfPuppets.GroupId\"\x7f\n\x0eMoveGroupQuery\x12\x32\n\x07groupId\x18\x01 \x02(\x0b\x32!.Devialet.MasterOfPuppets.GroupId\x12\x39\n\x0cnewBouquetId\x18\x02 \x02(\x0b\x32#.Devialet.MasterOfPuppets.BouquetId\"\x84\x01\n\x11MoveRendererQuery\x12\x38\n\nrendererId\x18\x01 \x02(\x0b\x32$.Devialet.MasterOfPuppets.RendererId\x12\x35\n\nnewGroupId\x18\x02 \x02(\x0b\x32!.Devialet.MasterOfPuppets.GroupId\"\'\n\x0bRenameQuery\x12\n\n\x02id\x18\x01 \x02(\x0c\x12\x0c\n\x04name\x18\x02 \x02(\t\"R\n\x18\x42ouquetAddedNotification\x12\x36\n\tbouquetId\x18\x01 \x02(\x0b\x32#.Devialet.MasterOfPuppets.BouquetId\"\x8c\x01\n\x16GroupAddedNotification\x12\x35\n\x08parentId\x18\x01 \x02(\x0b\x32#.Devialet.MasterOfPuppets.BouquetId\x12-\n\x02id\x18\x02 \x02(\x0b\x32!.Devialet.MasterOfPuppets.GroupId\x12\x0c\n\x04name\x18\x03 \x02(\t\"\xa5\x01\n\x19RendererAddedNotification\x12\x33\n\x08parentId\x18\x01 \x02(\x0b\x32!.Devialet.MasterOfPuppets.GroupId\x12\x30\n\x02id\x18\x02 \x02(\x0b\x32$.Devialet.MasterOfPuppets.RendererId\x12\x0c\n\x04name\x18\x03 \x02(\t\x12\x13\n\x0bisActivated\x18\x04 \x02(\x08\"b\n\x11StateNotification\x12\x38\n\nrendererId\x18\x01 \x02(\x0b\x32$.Devialet.MasterOfPuppets.RendererId\x12\x13\n\x0bisActivated\x18\x02 \x02(\x08\x32\x91\x10\n\rConfiguration\x12P\n\naddBouquet\x12\x1b.Devialet.CallMeMaybe.Empty\x1a#.Devialet.MasterOfPuppets.BouquetId\"\x00\x12S\n\rremoveBouquet\x12#.Devialet.MasterOfPuppets.BouquetId\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12X\n\x08\x61\x64\x64Group\x12\'.Devialet.MasterOfPuppets.AddGroupQuery\x1a!.Devialet.MasterOfPuppets.GroupId\"\x00\x12X\n\x0cisolateGroup\x12!.Devialet.MasterOfPuppets.GroupId\x1a#.Devialet.MasterOfPuppets.BouquetId\"\x00\x12T\n\tmoveGroup\x12(.Devialet.MasterOfPuppets.MoveGroupQuery\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12O\n\x0bremoveGroup\x12!.Devialet.MasterOfPuppets.GroupId\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12S\n\x0brenameGroup\x12%.Devialet.MasterOfPuppets.RenameQuery\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12X\n\x0b\x61\x64\x64Renderer\x12*.Devialet.MasterOfPuppets.AddRendererQuery\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12Z\n\x0cmoveRenderer\x12+.Devialet.MasterOfPuppets.MoveRendererQuery\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12U\n\x0eremoveRenderer\x12$.Devialet.MasterOfPuppets.RendererId\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12V\n\x0erenameRenderer\x12%.Devialet.MasterOfPuppets.RenameQuery\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12\x61\n\x0c\x62ouquetAdded\x12\x32.Devialet.MasterOfPuppets.BouquetAddedNotification\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12T\n\x0e\x62ouquetRemoved\x12#.Devialet.MasterOfPuppets.BouquetId\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12V\n\x0e\x62ouquetRenamed\x12%.Devialet.MasterOfPuppets.RenameQuery\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12]\n\ngroupAdded\x12\x30.Devialet.MasterOfPuppets.GroupAddedNotification\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12U\n\ngroupMoved\x12(.Devialet.MasterOfPuppets.MoveGroupQuery\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12P\n\x0cgroupRemoved\x12!.Devialet.MasterOfPuppets.GroupId\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12T\n\x0cgroupRenamed\x12%.Devialet.MasterOfPuppets.RenameQuery\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12\x63\n\rrendererAdded\x12\x33.Devialet.MasterOfPuppets.RendererAddedNotification\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12[\n\rrendererMoved\x12+.Devialet.MasterOfPuppets.MoveRendererQuery\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12V\n\x0frendererRemoved\x12$.Devialet.MasterOfPuppets.RendererId\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12W\n\x0frendererRenamed\x12%.Devialet.MasterOfPuppets.RenameQuery\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12\x62\n\x14rendererStateChanged\x12+.Devialet.MasterOfPuppets.StateNotification\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00')
  ,
  dependencies=[CallMeMaybe_dot_CommonMessages__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_GROUPID = _descriptor.Descriptor(
  name='GroupId',
  full_name='Devialet.MasterOfPuppets.GroupId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Devialet.MasterOfPuppets.GroupId.id', index=0,
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
  serialized_start=99,
  serialized_end=120,
)


_BOUQUETID = _descriptor.Descriptor(
  name='BouquetId',
  full_name='Devialet.MasterOfPuppets.BouquetId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Devialet.MasterOfPuppets.BouquetId.id', index=0,
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
  serialized_start=122,
  serialized_end=145,
)


_RENDERERID = _descriptor.Descriptor(
  name='RendererId',
  full_name='Devialet.MasterOfPuppets.RendererId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Devialet.MasterOfPuppets.RendererId.id', index=0,
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
  serialized_start=147,
  serialized_end=171,
)


_NODERENDERER = _descriptor.Descriptor(
  name='NodeRenderer',
  full_name='Devialet.MasterOfPuppets.NodeRenderer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rendererId', full_name='Devialet.MasterOfPuppets.NodeRenderer.rendererId', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='Devialet.MasterOfPuppets.NodeRenderer.name', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isActivated', full_name='Devialet.MasterOfPuppets.NodeRenderer.isActivated', index=2,
      number=3, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
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
  serialized_start=173,
  serialized_end=280,
)


_NODEGROUP = _descriptor.Descriptor(
  name='NodeGroup',
  full_name='Devialet.MasterOfPuppets.NodeGroup',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='groupId', full_name='Devialet.MasterOfPuppets.NodeGroup.groupId', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='Devialet.MasterOfPuppets.NodeGroup.name', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='renderers', full_name='Devialet.MasterOfPuppets.NodeGroup.renderers', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=283,
  serialized_end=419,
)


_NODEBOUQUET = _descriptor.Descriptor(
  name='NodeBouquet',
  full_name='Devialet.MasterOfPuppets.NodeBouquet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bouquetId', full_name='Devialet.MasterOfPuppets.NodeBouquet.bouquetId', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='groups', full_name='Devialet.MasterOfPuppets.NodeBouquet.groups', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  serialized_start=421,
  serialized_end=543,
)


_NODEROOT = _descriptor.Descriptor(
  name='NodeRoot',
  full_name='Devialet.MasterOfPuppets.NodeRoot',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bouquets', full_name='Devialet.MasterOfPuppets.NodeRoot.bouquets', index=0,
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
  serialized_start=545,
  serialized_end=612,
)


_ADDGROUPQUERY = _descriptor.Descriptor(
  name='AddGroupQuery',
  full_name='Devialet.MasterOfPuppets.AddGroupQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Devialet.MasterOfPuppets.AddGroupQuery.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bouquetId', full_name='Devialet.MasterOfPuppets.AddGroupQuery.bouquetId', index=1,
      number=2, type=11, cpp_type=10, label=2,
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
  serialized_start=614,
  serialized_end=699,
)


_ADDRENDERERQUERY = _descriptor.Descriptor(
  name='AddRendererQuery',
  full_name='Devialet.MasterOfPuppets.AddRendererQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rendererId', full_name='Devialet.MasterOfPuppets.AddRendererQuery.rendererId', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='Devialet.MasterOfPuppets.AddRendererQuery.name', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='groupId', full_name='Devialet.MasterOfPuppets.AddRendererQuery.groupId', index=2,
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
  serialized_start=702,
  serialized_end=844,
)


_MOVEGROUPQUERY = _descriptor.Descriptor(
  name='MoveGroupQuery',
  full_name='Devialet.MasterOfPuppets.MoveGroupQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='groupId', full_name='Devialet.MasterOfPuppets.MoveGroupQuery.groupId', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='newBouquetId', full_name='Devialet.MasterOfPuppets.MoveGroupQuery.newBouquetId', index=1,
      number=2, type=11, cpp_type=10, label=2,
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
  serialized_start=846,
  serialized_end=973,
)


_MOVERENDERERQUERY = _descriptor.Descriptor(
  name='MoveRendererQuery',
  full_name='Devialet.MasterOfPuppets.MoveRendererQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rendererId', full_name='Devialet.MasterOfPuppets.MoveRendererQuery.rendererId', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='newGroupId', full_name='Devialet.MasterOfPuppets.MoveRendererQuery.newGroupId', index=1,
      number=2, type=11, cpp_type=10, label=2,
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
  serialized_start=976,
  serialized_end=1108,
)


_RENAMEQUERY = _descriptor.Descriptor(
  name='RenameQuery',
  full_name='Devialet.MasterOfPuppets.RenameQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Devialet.MasterOfPuppets.RenameQuery.id', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='Devialet.MasterOfPuppets.RenameQuery.name', index=1,
      number=2, type=9, cpp_type=9, label=2,
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
  serialized_start=1110,
  serialized_end=1149,
)


_BOUQUETADDEDNOTIFICATION = _descriptor.Descriptor(
  name='BouquetAddedNotification',
  full_name='Devialet.MasterOfPuppets.BouquetAddedNotification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bouquetId', full_name='Devialet.MasterOfPuppets.BouquetAddedNotification.bouquetId', index=0,
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
  serialized_start=1151,
  serialized_end=1233,
)


_GROUPADDEDNOTIFICATION = _descriptor.Descriptor(
  name='GroupAddedNotification',
  full_name='Devialet.MasterOfPuppets.GroupAddedNotification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parentId', full_name='Devialet.MasterOfPuppets.GroupAddedNotification.parentId', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='id', full_name='Devialet.MasterOfPuppets.GroupAddedNotification.id', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='Devialet.MasterOfPuppets.GroupAddedNotification.name', index=2,
      number=3, type=9, cpp_type=9, label=2,
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
  serialized_start=1236,
  serialized_end=1376,
)


_RENDERERADDEDNOTIFICATION = _descriptor.Descriptor(
  name='RendererAddedNotification',
  full_name='Devialet.MasterOfPuppets.RendererAddedNotification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parentId', full_name='Devialet.MasterOfPuppets.RendererAddedNotification.parentId', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='id', full_name='Devialet.MasterOfPuppets.RendererAddedNotification.id', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='Devialet.MasterOfPuppets.RendererAddedNotification.name', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isActivated', full_name='Devialet.MasterOfPuppets.RendererAddedNotification.isActivated', index=3,
      number=4, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
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
  serialized_start=1379,
  serialized_end=1544,
)


_STATENOTIFICATION = _descriptor.Descriptor(
  name='StateNotification',
  full_name='Devialet.MasterOfPuppets.StateNotification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rendererId', full_name='Devialet.MasterOfPuppets.StateNotification.rendererId', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isActivated', full_name='Devialet.MasterOfPuppets.StateNotification.isActivated', index=1,
      number=2, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
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
  serialized_start=1546,
  serialized_end=1644,
)

_NODERENDERER.fields_by_name['rendererId'].message_type = _RENDERERID
_NODEGROUP.fields_by_name['groupId'].message_type = _GROUPID
_NODEGROUP.fields_by_name['renderers'].message_type = _NODERENDERER
_NODEBOUQUET.fields_by_name['bouquetId'].message_type = _BOUQUETID
_NODEBOUQUET.fields_by_name['groups'].message_type = _NODEGROUP
_NODEROOT.fields_by_name['bouquets'].message_type = _NODEBOUQUET
_ADDGROUPQUERY.fields_by_name['bouquetId'].message_type = _BOUQUETID
_ADDRENDERERQUERY.fields_by_name['rendererId'].message_type = _RENDERERID
_ADDRENDERERQUERY.fields_by_name['groupId'].message_type = _GROUPID
_MOVEGROUPQUERY.fields_by_name['groupId'].message_type = _GROUPID
_MOVEGROUPQUERY.fields_by_name['newBouquetId'].message_type = _BOUQUETID
_MOVERENDERERQUERY.fields_by_name['rendererId'].message_type = _RENDERERID
_MOVERENDERERQUERY.fields_by_name['newGroupId'].message_type = _GROUPID
_BOUQUETADDEDNOTIFICATION.fields_by_name['bouquetId'].message_type = _BOUQUETID
_GROUPADDEDNOTIFICATION.fields_by_name['parentId'].message_type = _BOUQUETID
_GROUPADDEDNOTIFICATION.fields_by_name['id'].message_type = _GROUPID
_RENDERERADDEDNOTIFICATION.fields_by_name['parentId'].message_type = _GROUPID
_RENDERERADDEDNOTIFICATION.fields_by_name['id'].message_type = _RENDERERID
_STATENOTIFICATION.fields_by_name['rendererId'].message_type = _RENDERERID
DESCRIPTOR.message_types_by_name['GroupId'] = _GROUPID
DESCRIPTOR.message_types_by_name['BouquetId'] = _BOUQUETID
DESCRIPTOR.message_types_by_name['RendererId'] = _RENDERERID
DESCRIPTOR.message_types_by_name['NodeRenderer'] = _NODERENDERER
DESCRIPTOR.message_types_by_name['NodeGroup'] = _NODEGROUP
DESCRIPTOR.message_types_by_name['NodeBouquet'] = _NODEBOUQUET
DESCRIPTOR.message_types_by_name['NodeRoot'] = _NODEROOT
DESCRIPTOR.message_types_by_name['AddGroupQuery'] = _ADDGROUPQUERY
DESCRIPTOR.message_types_by_name['AddRendererQuery'] = _ADDRENDERERQUERY
DESCRIPTOR.message_types_by_name['MoveGroupQuery'] = _MOVEGROUPQUERY
DESCRIPTOR.message_types_by_name['MoveRendererQuery'] = _MOVERENDERERQUERY
DESCRIPTOR.message_types_by_name['RenameQuery'] = _RENAMEQUERY
DESCRIPTOR.message_types_by_name['BouquetAddedNotification'] = _BOUQUETADDEDNOTIFICATION
DESCRIPTOR.message_types_by_name['GroupAddedNotification'] = _GROUPADDEDNOTIFICATION
DESCRIPTOR.message_types_by_name['RendererAddedNotification'] = _RENDERERADDEDNOTIFICATION
DESCRIPTOR.message_types_by_name['StateNotification'] = _STATENOTIFICATION

GroupId = _reflection.GeneratedProtocolMessageType('GroupId', (_message.Message,), dict(
  DESCRIPTOR = _GROUPID,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.GroupId)
  ))
_sym_db.RegisterMessage(GroupId)

BouquetId = _reflection.GeneratedProtocolMessageType('BouquetId', (_message.Message,), dict(
  DESCRIPTOR = _BOUQUETID,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.BouquetId)
  ))
_sym_db.RegisterMessage(BouquetId)

RendererId = _reflection.GeneratedProtocolMessageType('RendererId', (_message.Message,), dict(
  DESCRIPTOR = _RENDERERID,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.RendererId)
  ))
_sym_db.RegisterMessage(RendererId)

NodeRenderer = _reflection.GeneratedProtocolMessageType('NodeRenderer', (_message.Message,), dict(
  DESCRIPTOR = _NODERENDERER,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.NodeRenderer)
  ))
_sym_db.RegisterMessage(NodeRenderer)

NodeGroup = _reflection.GeneratedProtocolMessageType('NodeGroup', (_message.Message,), dict(
  DESCRIPTOR = _NODEGROUP,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.NodeGroup)
  ))
_sym_db.RegisterMessage(NodeGroup)

NodeBouquet = _reflection.GeneratedProtocolMessageType('NodeBouquet', (_message.Message,), dict(
  DESCRIPTOR = _NODEBOUQUET,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.NodeBouquet)
  ))
_sym_db.RegisterMessage(NodeBouquet)

NodeRoot = _reflection.GeneratedProtocolMessageType('NodeRoot', (_message.Message,), dict(
  DESCRIPTOR = _NODEROOT,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.NodeRoot)
  ))
_sym_db.RegisterMessage(NodeRoot)

AddGroupQuery = _reflection.GeneratedProtocolMessageType('AddGroupQuery', (_message.Message,), dict(
  DESCRIPTOR = _ADDGROUPQUERY,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.AddGroupQuery)
  ))
_sym_db.RegisterMessage(AddGroupQuery)

AddRendererQuery = _reflection.GeneratedProtocolMessageType('AddRendererQuery', (_message.Message,), dict(
  DESCRIPTOR = _ADDRENDERERQUERY,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.AddRendererQuery)
  ))
_sym_db.RegisterMessage(AddRendererQuery)

MoveGroupQuery = _reflection.GeneratedProtocolMessageType('MoveGroupQuery', (_message.Message,), dict(
  DESCRIPTOR = _MOVEGROUPQUERY,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.MoveGroupQuery)
  ))
_sym_db.RegisterMessage(MoveGroupQuery)

MoveRendererQuery = _reflection.GeneratedProtocolMessageType('MoveRendererQuery', (_message.Message,), dict(
  DESCRIPTOR = _MOVERENDERERQUERY,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.MoveRendererQuery)
  ))
_sym_db.RegisterMessage(MoveRendererQuery)

RenameQuery = _reflection.GeneratedProtocolMessageType('RenameQuery', (_message.Message,), dict(
  DESCRIPTOR = _RENAMEQUERY,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.RenameQuery)
  ))
_sym_db.RegisterMessage(RenameQuery)

BouquetAddedNotification = _reflection.GeneratedProtocolMessageType('BouquetAddedNotification', (_message.Message,), dict(
  DESCRIPTOR = _BOUQUETADDEDNOTIFICATION,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.BouquetAddedNotification)
  ))
_sym_db.RegisterMessage(BouquetAddedNotification)

GroupAddedNotification = _reflection.GeneratedProtocolMessageType('GroupAddedNotification', (_message.Message,), dict(
  DESCRIPTOR = _GROUPADDEDNOTIFICATION,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.GroupAddedNotification)
  ))
_sym_db.RegisterMessage(GroupAddedNotification)

RendererAddedNotification = _reflection.GeneratedProtocolMessageType('RendererAddedNotification', (_message.Message,), dict(
  DESCRIPTOR = _RENDERERADDEDNOTIFICATION,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.RendererAddedNotification)
  ))
_sym_db.RegisterMessage(RendererAddedNotification)

StateNotification = _reflection.GeneratedProtocolMessageType('StateNotification', (_message.Message,), dict(
  DESCRIPTOR = _STATENOTIFICATION,
  __module__ = 'MasterOfPuppets.Configuration_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.MasterOfPuppets.StateNotification)
  ))
_sym_db.RegisterMessage(StateNotification)


# @@protoc_insertion_point(module_scope)