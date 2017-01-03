# -*- coding=utf8 -*-
"""语法解析"""
from protoparser.exc import ProtoGrammarError


def p_error(p):
    if p is None:
        raise ProtoGrammarError('grammar error at EOF')
    raise ProtoGrammarError('grammar error {} at line {}'.format(
        p.value, p.lineno))


def p_start(p):
    """start : header definition"""


def p_header(p):
    """header : header_unit_ header
              |"""


def p_header_unit_(p):
    """header_unit_ : header_unit ';'
                    | header_unit"""


def p_header_unit(p):
    """header_unit : syntax
                   | package"""


def p_syntax(p):
    """syntax : SYNTAX '=' IDENTIFIER"""


def p_package(p):
    """package : PACKAGE IDENTIFIER"""


def p_definition(p):
    """definition : definition definition_unit_
                  |"""


def p_definition_unit_(p):
    """definition_unit_ : definition_unit ';'
                        | definition_unit"""


def p_definition_unit(p):
    """definition_unit : service
                       | message"""


def p_message(p):
    """message : seen_message '{' field_seq '}'"""


def p_seen_message(p):
    """seen_message : MESSAGE IDENTIFIER"""


def p_field_seq(p):
    """field_seq : field ';' field_seq
                 |'"""


def p_field(p):
    """field : field_req field_type IDENTIFIER '=' INTCONSTANT"""


def p_field_req(p):
    """field_req : REQUIRED
                 | OPTIONAL
                 | REPEATED
                 |"""


def p_field_type(p):
    """field_type : ref_type
                  |  definition_type"""


def p_ref_type(p):
    """ref_type : IDENTIFIER"""


def p_definition_type(p):
    """definition_type : base_type
                       | container_type"""


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


def p_container_type(p):
    """container_type : map_type"""


def p_map_type(p):
    """map_type: MAP '<' field_type ',' field_type '>'"""


def p_service(p):
    """service : SERVICE IDENTIFIER '{' func_seq '}'"""


def p_func_seq(p):
    """func_seq : func func_seq
                | func ';' func_seq
                |"""


def p_func(p):
    """func : RPC IDENTIFIER '(' IDENTIFIER ')' RETURNS '(' IDENTIFIER ')' '{' '}'"""
