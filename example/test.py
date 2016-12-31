from ply import (
    lex,
    yacc,
)

literals = '.'


def t_error(t):
    raise Exception('error {} at line {}'.format(t.value[0], t.lineno))


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t


tokens = ('IDENTIFIER', )


def p_start(p):
    """start : dot_identifier"""


def p_dot_identifier(p):
    """dot_identifier : IDENTIFIER '.' dot_identifier
                      | IDENTIFIER"""
    print p.__dict__

if __name__ == '__main__':
    lexer = lex.lex()
    # lexer.input('www.baidu.com')
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break
    #     print tok
    parser = yacc.yacc(debug=True)

    lexer.lineno = 1
    parser.parse('www.baidu.com')
