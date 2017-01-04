# -*- coding=utf8 -*-
"""解析文件"""
import os
from ply import (
    yacc,
    lex,
)

from protoparser.lexer import *
from protoparser.grammar import *


def parse(proto_path, lexer=None, parser=None):
    """解析protobuf文件

    Args:
        proto_path (string): protobuf文件路径
        lexer (Lexer): 词法分析
        parser (Parser): 语法分析器
    """
    proto_path = os.path.abspath(proto_path)
    file_name = os.path.basename(proto_path)

    with open(proto_path, 'r') as pf:
        data = pf.read()

    if not lexer:
        lexer = lex.lex()
    if not parser:
        parser = yacc.yacc(debug=False, write_tables=0)

    lexer.lineno = 1
    result = parser.parse(data)
    result.filename = file_name
    return result
