# -*- coding=utf8 -*-
"""异常定义"""


class ProtoParserError(Exception):
    """解析错误基类"""
    pass


class ProtoLexerError(ProtoParserError):
    """词法解析错误"""
    pass


class ProtoGrammarError(ProtoParserError):
    """语法解析错误"""
    pass
