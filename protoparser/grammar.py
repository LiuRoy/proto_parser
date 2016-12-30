# -*- coding=utf8 -*-
"""语法解析"""
from protoparser.exc import ProtoGrammarError


def p_error(p):
    if p is None:
        raise ProtoGrammarError('grammar error at EOF')
    raise ProtoGrammarError('grammar error {} at line {}'.format(
        p.value, p.lineno))
