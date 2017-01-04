# -*- coding=utf8 -*-
"""语法解析"""
from protoparser.exc import ProtoGrammarError
from protoparser.objects import (
    MessageField,
    ServiceMethod,
    MapField,
    field_map,
    Service,
    Message,
    Protobuf,
)


class FieldType(object):
    """field类型"""
    BASE = 1
    MAP = 2
    REF = 3


class HeaderType(object):
    """header类型"""
    SYNTAX = 'syntax'
    PACKAGE = 'package'


def p_error(p):
    if p is None:
        raise ProtoGrammarError('grammar error at EOF')
    raise ProtoGrammarError('grammar error: {} at line {}'.format(
        p.value, p.lineno))


def p_start(p):
    """start : header definition"""
    package, syntax = '', 'proto3'
    for item in p[1]:
        if item[0] == HeaderType.SYNTAX:
            syntax = item[1]
        elif item[0] == HeaderType.PACKAGE:
            package = item[1]

    proto = Protobuf(package, syntax)
    symbols = set()
    for item in p[2]:
        item_name = item.name
        if item_name in symbols:
            raise ProtoGrammarError(
                'grammar error: symbol {} is already defined at line {}'.format(
                    item_name, p.lineno))

        if isinstance(item, Service):
            proto.services[item_name] = item
        elif isinstance(item, Message):
            proto.messages[item_name] = item
        symbols.add(item_name)

    _check_methods(proto)
    _update_fields(proto)
    p[0] = proto


def p_header(p):
    """header : header_unit_ header
              |"""
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]


def p_header_unit_(p):
    """header_unit_ : header_unit ';'
                    | header_unit"""
    p[0] = p[1]


def p_header_unit(p):
    """header_unit : syntax
                   | package"""
    p[0] = p[1]


def p_syntax(p):
    """syntax : SYNTAX '=' LITERAL"""
    if p[3] != 'proto3':
        raise ProtoGrammarError(
            'grammar error at line {}: syntax must be proto3'.format(p.lineno))
    p[0] = (HeaderType.SYNTAX, p[3])


def p_package(p):
    """package : PACKAGE IDENTIFIER"""
    p[0] = (HeaderType.PACKAGE, p[2])


def p_definition(p):
    """definition : definition definition_unit_
                  |"""
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[2]] + p[1]


def p_definition_unit_(p):
    """definition_unit_ : definition_unit ';'
                        | definition_unit"""
    p[0] = p[1]


def p_definition_unit(p):
    """definition_unit : service
                       | message"""
    p[0] = p[1]


def p_message(p):
    """message : seen_message '{' field_seq '}'"""
    message = Message(p[1])
    for index, field in enumerate(p[3]):
        optional, type_, name, number = field

        if name in message.fields:
            raise ProtoGrammarError(
                'grammar error: message {} is already defined at line {}'.format(
                    name, p.lineno))

        label = 1
        if optional == 'repeated':
            label = 3

        message_type = None
        if type_[0] == FieldType.BASE:
            class_ = field_map[type_[1]]
            field = class_(name, index, number, label,
                           message_type=message_type)
            if label == 3:
                field.default_value = []
        elif type_[0] == FieldType.MAP:
            label = 3
            field = MapField(name, index, number, label,
                             message_type=message_type,
                             key_type=type_[2],
                             value_type=type_[3])
            field.default_value = []
        else:
            field = MessageField(name, index, number, label,
                                 message_type=type_[1])
        message.fields[name] = field

    p[0] = message


def p_seen_message(p):
    """seen_message : MESSAGE IDENTIFIER"""
    p[0] = p[2]


def p_field_seq(p):
    """field_seq : field ';' field_seq
                 |"""
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[3]


def p_field(p):
    """field : field_req field_type IDENTIFIER '=' INTCONSTANT"""
    p[0] = (p[1], p[2], p[3], p[5])


def p_field_req(p):
    """field_req : OPTIONAL
                 | REPEATED
                 |"""
    if len(p) == 2 and p[1] == 'repeated':
        p[0] = 'repeated'
    else:
        p[0] = 'optional'


def p_field_type(p):
    """field_type : ref_type
                  |  definition_type"""
    p[0] = p[1]


def p_ref_type(p):
    """ref_type : IDENTIFIER"""
    p[0] = (FieldType.REF, p[1])


def p_definition_type(p):
    """definition_type : base_type
                       | container_type"""
    p[0] = p[1]


def p_base_type(p):
    """base_type : BOOL
                 | STRING
                 | BYTES
                 | DOUBLE
                 | FLOAT
                 | INT32
                 | INT64
                 | UINT32
                 | UINT64
                 | SINT32
                 | SINT64
                 | FIXED32
                 | FIXED64
                 | SFIXED32
                 | SFIXED64"""
    p[0] = (FieldType.BASE, p[1])


def p_container_type(p):
    """container_type : map_type"""
    p[0] = p[1]


def p_map_type(p):
    """map_type : MAP '<' base_type ',' base_type '>'
               | MAP '<' base_type ',' ref_type '>'"""
    if p[3] == 'bytes':
        raise ProtoGrammarError(
            'grammar error at line {}: key type cannot be bytes'.format(p.lineno))
    p[0] = (FieldType.MAP, p[1], p[3], p[5])


def p_service(p):
    """service : SERVICE IDENTIFIER '{' func_seq '}'"""
    service = Service(p[2])
    for method in p[4]:
        if method.name in service.methods:
            raise ProtoGrammarError(
                'grammar error: method {} is already defined at line {}'.format(
                    method.name, p.lineno))
        service.methods[method.name] = method
    p[0] = service


def p_func_seq(p):
    """func_seq : func func_seq
                | func ';' func_seq
                |"""
    p_len = len(p)
    if p_len == 1:
        p[0] = []
    elif p_len == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]] + p[3]


def p_func(p):
    """func : RPC IDENTIFIER '(' IDENTIFIER ')' RETURNS '(' IDENTIFIER ')' '{' '}'"""
    p[0] = ServiceMethod(p[2], p[4], p[8])


def _check_methods(proto):
    """检查serivce中定义方法的传参能否解析

    Args:
        proto (Protobuf): 解析得到的对象
    """
    for _, service in proto.services.iteritems():
        for method_name, method in service.methods.iteritems():
            if method.request_type in proto.messages and \
                            method.response_type in proto.messages:
                continue
            raise ProtoGrammarError(
                'grammar error: {} params not defined'.format(method_name,))


def _update_fields(proto):
    """更新map中的自定义类型以及检查嵌套message类型是否存在

    Args:
        proto (Protobuf): 解析得到的对象
    """
    for _, message in proto.messages.iteritems():
        for field_name, field in message.fields.iteritems():
            if isinstance(field, MessageField):
                if field_name not in proto.messages:
                    raise ProtoGrammarError(
                        'grammar error: {} not defined'.format(field_name))

                field.message_type = proto.messages[field_name]
            elif isinstance(field, MapField):
                key_type, key_name = field.key_type
                val_type, val_name = field.value_type

                if val_type == FieldType.REF:
                    if val_name not in proto.messages:
                        raise ProtoGrammarError(
                            'grammar error: {} not defined'.format(field_name))

                    field.value_type = MessageField(
                        val_name, 1, 1, 1, proto.messages[val_name])
                else:
                    class_ = field_map[val_name]
                    field.value_type = class_('value', 1, 1, 1)

                class_ = field_map[key_name]
                field.key_type = class_('key', 0, 0, 1)
