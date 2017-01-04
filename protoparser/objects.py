# -*- coding=utf8 -*-
"""protofuf 对象定义"""


class Field(object):
    """字段类型父类"""

    def __init__(self, name, index, number, label,
                 message_type=None,):
        self.name = name
        self.index = index
        self.number = number
        self.label = label
        self.message_type = message_type


class BoolField(Field):
    """bool类型"""
    type = 8
    cpp_type = 7
    default_value = False


class StringField(Field):
    """string类型"""
    type = 9
    cpp_type = 9
    default_value = u''


class BytesField(Field):
    """bytes类型"""
    type = 12
    cpp_type = 9
    default_value = ''


class DoubleField(Field):
    """double类型"""
    type = 1
    cpp_type = 5
    default_value = 0.0


class FloatField(Field):
    """float类型"""
    type = 2
    cpp_type = 6
    default_value = 0.0


class Int32Field(Field):
    """int32类型"""
    type = 5
    cpp_type = 1
    default_value = 0


class Int64Field(Field):
    """int64类型"""
    type = 3
    cpp_type = 2
    default_value = 0


class Uint32Field(Field):
    """uint32类型"""
    type = 13
    cpp_type = 3
    default_value = 0


class Uint64Field(Field):
    """uint64类型"""
    type = 4
    cpp_type = 4
    default_value = 0


class Sint32Field(Field):
    """sint32类型"""
    type = 17
    cpp_type = 1
    default_value = 0


class Sint64Field(Field):
    """sint64类型"""
    type = 18
    cpp_type = 2
    default_value = 0


class Fixed32Field(Field):
    """fixed32类型"""
    type = 7
    cpp_type = 3
    default_value = 0


class Fixed64Field(Field):
    """fixed32类型"""
    type = 6
    cpp_type = 4
    default_value = 0


class Sfixed32Field(Field):
    """sfixed32类型"""
    type = 15
    cpp_type = 1
    default_value = 0


class Sfixed64Field(Field):
    """sfixed64类型"""
    type = 16
    cpp_type = 2
    default_value = 0


class MessageField(Field):
    """message类型"""
    type = 11
    cpp_type = 10
    default_value = None


class MapField(Field):
    """map类型"""
    type = 11
    cpp_type = 10
    default_value = []

    def __init__(self, name, index, number, label,
                 message_type=None, key_type=None, value_type=None):
        self.key_type = key_type
        self.value_type = value_type
        super(MapField, self).__init__(
            name, index, number, label, message_type)


field_map = {
    'bool': BoolField,
    'string': StringField,
    'bytes': BytesField,
    'double': DoubleField,
    'float': FloatField,
    'int32': Int32Field,
    'int64': Int64Field,
    'uint32': Uint32Field,
    'uint64': Uint64Field,
    'sint32': Sint32Field,
    'sint64': Sint64Field,
    'fixed32': Fixed32Field,
    'fixed64': Fixed64Field,
    'sfixed32': Sfixed32Field,
    'sfixed64': Sfixed64Field,
}


class ServiceMethod(object):
    """service rpc method"""
    def __init__(self, name, request_type, response_type):
        self.name = name
        self.request_type = request_type
        self.response_type = response_type


class Service(object):
    """service"""
    def __init__(self, name, methods=None):
        self.name = name
        self.methods = methods or {}


class Message(object):
    """message"""
    def __init__(self, name, fields=None):
        self.name = name
        self.fields = fields or {}


class Protobuf(object):
    """解析的对象"""

    def __init__(self, package='', syntax='proto3'):
        self.package = package
        self.syntax = syntax

        self.services = {}
        self.messages = {}
        self.filename = None
