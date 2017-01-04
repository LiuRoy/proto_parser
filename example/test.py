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
    p[0] = p[1]


def p_dot_identifier(p):
    """dot_identifier : IDENTIFIER '.' dot_identifier
                      | IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]

if __name__ == '__main__':
    lexer = lex.lex()
    parser = yacc.yacc(debug=True)

    lexer.lineno = 1
    s = parser.parse('www.baidu.com')
    print s
