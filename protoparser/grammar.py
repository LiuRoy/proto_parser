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
    """package : PACKAGE dot_identifier"""


def dot_identifier(p):
    """dot_identifier : IDENTIFIER '.' dot_identifier
                      | IDENTIFIER"""


def p_sep(p):
    """sep : ','
           | ';'
    """
