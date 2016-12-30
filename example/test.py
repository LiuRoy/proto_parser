from ply import (
    lex,
    yacc,
)

literals = '.'


def t_IDENTIFIER(t):
    r'[a-zA-Z_](\.[a-zA-Z_0-9]|[a-zA-Z_0-9])*'


tokens = ('IDENTIFIER', )


def p_start(p):
    """start : dot_identifier"""


def p_dot_identifier(p):
    """dot_identifier : IDENTIFIER '.' dot_identifier
                      | IDENTIFIER"""
    print p[1]

if __name__ == '__main__':
    lexer = lex.lex()
    parser = yacc.yacc(debug=True)

    lexer.lineno = 1
    parser.parse('www.baidu.com')
