# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: databroker.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='databroker.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x10\x64\x61tabroker.proto\x1a\x1bgoogle/protobuf/empty.proto\"5\n\x08\x45LG_Text\x12\x11\n\tPlainText\x18\x01 \x01(\t\x12\x16\n\x0eStructuredText\x18\x02 \x01(\t2B\n\x11Transfer_ELG_Text\x12-\n\x08get_Text\x12\x16.google.protobuf.Empty\x1a\t.ELG_Textb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_ELG_TEXT = _descriptor.Descriptor(
  name='ELG_Text',
  full_name='ELG_Text',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='PlainText', full_name='ELG_Text.PlainText', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='StructuredText', full_name='ELG_Text.StructuredText', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=49,
  serialized_end=102,
)

DESCRIPTOR.message_types_by_name['ELG_Text'] = _ELG_TEXT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ELG_Text = _reflection.GeneratedProtocolMessageType('ELG_Text', (_message.Message,), {
  'DESCRIPTOR' : _ELG_TEXT,
  '__module__' : 'databroker_pb2'
  # @@protoc_insertion_point(class_scope:ELG_Text)
  })
_sym_db.RegisterMessage(ELG_Text)



_TRANSFER_ELG_TEXT = _descriptor.ServiceDescriptor(
  name='Transfer_ELG_Text',
  full_name='Transfer_ELG_Text',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=104,
  serialized_end=170,
  methods=[
  _descriptor.MethodDescriptor(
    name='get_Text',
    full_name='Transfer_ELG_Text.get_Text',
    index=0,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_ELG_TEXT,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TRANSFER_ELG_TEXT)

DESCRIPTOR.services_by_name['Transfer_ELG_Text'] = _TRANSFER_ELG_TEXT

# @@protoc_insertion_point(module_scope)