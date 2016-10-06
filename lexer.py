from ply import lex

tokens = [
        'NUMBER',
        'VARIABLE',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
        'EQUALS',
        'POWER',
        'LOG',
        ]
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_POWER  = r'\^'
t_LOG = '_log'
t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_VARIABLE(t):
    r'[a-zA-Z]'
    t.value = str(t.value)
    return t

def t_error(t):
    print('Illegal token %s found' % (t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()
