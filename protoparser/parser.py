# -*- coding=utf8 -*-
"""解析文件"""
import os
import types
from ply import (
    yacc,
    lex,
)
from google.protobuf import (
    descriptor as _descriptor,
    message as _message,
    reflection as _reflection,
    symbol_database as _symbol_database
)

from protoparser.lexer import *
from protoparser.grammar import *


def load(proto_path, lexer=None, parser=None):
    """解析protobuf文件

    Args:
        proto_path (string): protobuf文件路径
        lexer (Lexer): 词法分析
        parser (Parser): 语法分析器
    """
    proto_path = os.path.abspath(proto_path)

    if not proto_path.endswith('.proto'):
        raise Exception('file name must end with .proto')

    with open(proto_path, 'r') as pf:
        data = pf.read()

    if not lexer:
        lexer = lex.lex()
    if not parser:
        parser = yacc.yacc(debug=False, write_tables=0)

    lexer.lineno = 1
    result = parser.parse(data)
    result.filename = proto_path
    return result


def transform(proto):
    """把load生成的对象转换为原生对象

    Args:
        proto (Protobuf): load返回对象
    """
    file_name = os.path.basename(proto.filename)
    module_name = file_name.replace('.proto', '_pb2')
    proto_module = types.ModuleType(module_name)

    proto_module._sym_db = _symbol_database.Default()
    descriptor = _descriptor.FileDescriptor(
        name=file_name,
        package=proto.package,
        syntax=proto.package,
        serialized_pb=''
    )
    proto_module._sym_db.RegisterFileDescriptor(descriptor)

    # serialized_start和serialized_end真不知道怎么算出来的, 这里就简单的估算一下
    serialized_start = serialized_end = 23 + len(proto.package)
    descriptor_map = {}
    for message_name, message in proto.messages.iteritems():
        fields = []
        for field_name, field in message.fields.iteritems():
            if fields:
                serialized_end += 15
            else:
                serialized_end += 25

            fields.append(_descriptor.FieldDescriptor(
                name=field_name,
                full_name='.'.join((proto.package, message_name, field_name)),
                index=field.index,
                number=field.number,
                type=field.type,
                cpp_type=field.cpp_type,
                label=field.label,
                has_default_value=False,
                default_value=field.default_value,
                message_type=None,
                enum_type=None,
                containing_type=None,
                is_extension=False,
                extension_scope=None,
                options=None,
            ))

        descriptor_map[message_name] = _descriptor.Descriptor(
            name=message_name,
            full_name='.'.join((proto.package, message_name)),
            filename=None,
            file=descriptor,
            containing_type=None,
            fields=fields,
            extensions=[],
            nested_types=[],
            enum_types=[],
            options=None,
            is_extendable=False,
            syntax=proto.syntax,
            extension_ranges=[],
            oneofs=[],
            serialized_start=serialized_start,
            serialized_end=serialized_end,
        )
        serialized_start = serialized_end = serialized_end + 2

    for descriptor_name, des in descriptor_map.iteritems():
        descriptor.message_types_by_name[descriptor_name] = des
        setattr(proto_module, descriptor_name,
                _reflection.GeneratedProtocolMessageType(
                    descriptor_name,
                    (_message.Message,),
                    {
                        'DESCRIPTOR': des,
                        '__module__': module_name
                    }
                ))
        proto_module._sym_db.RegisterMessage(
            getattr(proto_module, descriptor_name))

    return proto_module


def make_client(proto_path):
    """根据protobuf文件直接生成客户端相关对象"""
    proto = load(proto_path)
    proto_module = transform(proto)

    for service_name, service in proto.services.iteritems():
        class_name = '{}Stub'.format(service_name)

        def init_method(self, channel):
            for method_name, method in service.methods.iteritems():
                setattr(self, method_name, channel.unary_unary(
                    '/{}/{}'.format('.'.join((proto.package, service_name)),
                                    method_name),
                    request_serializer=getattr(
                        proto_module, method.request_type).SerializeToString,
                    response_deserializer=getattr(
                        proto_module, method.response_type).FromString,
                ))

        stub_class = type(class_name, (object,), {
            '__module__': proto_module.__name__,
            '__init__': init_method
        })
        setattr(proto_module, class_name, stub_class)

    return proto_module
