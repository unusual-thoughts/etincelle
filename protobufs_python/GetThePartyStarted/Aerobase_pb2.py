# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: GetThePartyStarted/Aerobase.proto

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
from GetThePartyStarted import GetThePartyStarted_pb2 as GetThePartyStarted_dot_GetThePartyStarted__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='GetThePartyStarted/Aerobase.proto',
  package='Devialet.GetThePartyStarted.Aerobase',
  syntax='proto2',
  serialized_pb=_b('\n!GetThePartyStarted/Aerobase.proto\x12$Devialet.GetThePartyStarted.Aerobase\x1a CallMeMaybe/CommonMessages.proto\x1a+GetThePartyStarted/GetThePartyStarted.proto\"\xa8\x03\n\tSetupStep\x12\x0c\n\x04step\x18\x01 \x02(\r\"\x8c\x03\n\x04Step\x12\x0f\n\x0bInvalidStep\x10\x00\x12\x0f\n\x0bInitialStep\x10\x01\x12\x1d\n\x19\x43onfigureSetupNetworkStep\x10\x02\x12\x13\n\x0fWaitForUserStep\x10\x03\x12\x15\n\x11WaitForSlavesStep\x10\x04\x12\x17\n\x13\x41ssociateSlavesStep\x10\x05\x12\x1f\n\x1bWaitForSlaveAssociationStep\x10\x06\x12\x18\n\x14\x41ssociatingSlaveStep\x10\x07\x12\x19\n\x15\x43onfiguringSlavesStep\x10\x08\x12\"\n\x1e\x43onfigureProductionNetworkStep\x10\t\x12\x1f\n\x1bWaitForConfiguredSlavesStep\x10\n\x12\x1b\n\x17\x41llSlavesConfiguredStep\x10\x0b\x12\x19\n\x15\x43onfigureTopologyStep\x10\x0c\x12\x19\n\x15\x43onfigureServicesStep\x10\r\x12\x10\n\x0c\x43ompleteStep\x10\x0e\"A\n\x1fSetTopologyConfigurationRequest\x12\x10\n\x08masterId\x18\x01 \x02(\x0c\x12\x0c\n\x04\x64\x61ta\x18\x02 \x02(\x0c\x32\x0f\n\rConfiguration2\xc4\x02\n\x05Setup\x12[\n\x11\x63onfigureTopology\x12\'.Devialet.GetThePartyStarted.SetupToken\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12\x80\x01\n\x18setTopologyConfiguration\x12\x45.Devialet.GetThePartyStarted.Aerobase.SetTopologyConfigurationRequest\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00\x12[\n\x11\x63onfigureServices\x12\'.Devialet.GetThePartyStarted.SetupToken\x1a\x1b.Devialet.CallMeMaybe.Empty\"\x00')
  ,
  dependencies=[CallMeMaybe_dot_CommonMessages__pb2.DESCRIPTOR,GetThePartyStarted_dot_GetThePartyStarted__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_SETUPSTEP_STEP = _descriptor.EnumDescriptor(
  name='Step',
  full_name='Devialet.GetThePartyStarted.Aerobase.SetupStep.Step',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='InvalidStep', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='InitialStep', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ConfigureSetupNetworkStep', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WaitForUserStep', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WaitForSlavesStep', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AssociateSlavesStep', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WaitForSlaveAssociationStep', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AssociatingSlaveStep', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ConfiguringSlavesStep', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ConfigureProductionNetworkStep', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WaitForConfiguredSlavesStep', index=10, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AllSlavesConfiguredStep', index=11, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ConfigureTopologyStep', index=12, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ConfigureServicesStep', index=13, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CompleteStep', index=14, number=14,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=183,
  serialized_end=579,
)
_sym_db.RegisterEnumDescriptor(_SETUPSTEP_STEP)


_SETUPSTEP = _descriptor.Descriptor(
  name='SetupStep',
  full_name='Devialet.GetThePartyStarted.Aerobase.SetupStep',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='step', full_name='Devialet.GetThePartyStarted.Aerobase.SetupStep.step', index=0,
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
    _SETUPSTEP_STEP,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=155,
  serialized_end=579,
)


_SETTOPOLOGYCONFIGURATIONREQUEST = _descriptor.Descriptor(
  name='SetTopologyConfigurationRequest',
  full_name='Devialet.GetThePartyStarted.Aerobase.SetTopologyConfigurationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='masterId', full_name='Devialet.GetThePartyStarted.Aerobase.SetTopologyConfigurationRequest.masterId', index=0,
      number=1, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='Devialet.GetThePartyStarted.Aerobase.SetTopologyConfigurationRequest.data', index=1,
      number=2, type=12, cpp_type=9, label=2,
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
  serialized_start=581,
  serialized_end=646,
)

_SETUPSTEP_STEP.containing_type = _SETUPSTEP
DESCRIPTOR.message_types_by_name['SetupStep'] = _SETUPSTEP
DESCRIPTOR.message_types_by_name['SetTopologyConfigurationRequest'] = _SETTOPOLOGYCONFIGURATIONREQUEST

SetupStep = _reflection.GeneratedProtocolMessageType('SetupStep', (_message.Message,), dict(
  DESCRIPTOR = _SETUPSTEP,
  __module__ = 'GetThePartyStarted.Aerobase_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.GetThePartyStarted.Aerobase.SetupStep)
  ))
_sym_db.RegisterMessage(SetupStep)

SetTopologyConfigurationRequest = _reflection.GeneratedProtocolMessageType('SetTopologyConfigurationRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETTOPOLOGYCONFIGURATIONREQUEST,
  __module__ = 'GetThePartyStarted.Aerobase_pb2'
  # @@protoc_insertion_point(class_scope:Devialet.GetThePartyStarted.Aerobase.SetTopologyConfigurationRequest)
  ))
_sym_db.RegisterMessage(SetTopologyConfigurationRequest)


# @@protoc_insertion_point(module_scope)
