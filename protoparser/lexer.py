# -*- coding=utf8 -*-
"""词法解析"""
from protoparser.exc import ProtoLexerError


literals = '.;,={}<>[]()'

# enum packed singular import reserved option oneof等暂不支持
keywords = (
    'syntax',
    'package',
    'message',
    'required',
    'optional',
    'repeated',
    'double',
    'float',
    'int32',
    'int64',
    'uint32',
    'uint64',
    'sint32',
    'sint64',
    'fixed32',
    'fixed64',
    'sfixed32',
    'sfixed64',
    'bool',
    'string',
    'bytes',
    'map',
    'service',
    'rpc',
    'returns'
)

tokens = (
    'INTCONSTANT',
    'LITERAL',
    'IDENTIFIER',
) + tuple(map(lambda kw: kw.upper(), keywords))

t_ignore = ' \t\r'


def t_error(t):
    raise ProtoLexerError('illegal character {} at line {}'.format(
        t.value[0], t.lineno))


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_ignore_COMMENT(t):
    r'\/\/[^\n]*'


def t_HEXCONSTANT(t):
    r'0x[0-9A-Fa-f]+'
    t.value = int(t.value, 16)
    t.type = 'INTCONSTANT'
    return t


def t_INTCONSTANT(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t


def t_LITERAL(t):
    r'(\"([^\\\n]|(\\.))*?\")|\'([^\\\n]|(\\.))*?\''
    s = t.value[1:-1]
    maps = {
        't': '\t',
        'r': '\r',
        'n': '\n',
        '\\': '\\',
        '\'': '\'',
        '"': '\"'
    }
    i = 0
    length = len(s)
    val = ''
    while i < length:
        if s[i] == '\\':
            i += 1
            if s[i] in maps:
                val += maps[s[i]]
            else:
                msg = 'unexpected escaping character: {}'.format(s[i])
                raise ProtoLexerError(msg)
        else:
            val += s[i]

        i += 1

    t.value = val
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_](\.[a-zA-Z_0-9]|[a-zA-Z_0-9])*'

    if t.value in keywords:
        t.type = t.value.upper()
    return t
