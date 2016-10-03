from ply import yacc
import lexer
from ast import ASTNode

tokens = lexer.tokens

def p_equality_expression_1(p):
    '''
    equality_expression : add_expression
    '''
    p[0] = p[1]

def p_equality_expression_2(p):
    '''
    equality_expression : equality_expression EQUALS add_expression 
    '''
    p[0] = ASTNode('equality_expression', p[2], [ p[1], p[3] ])

def p_add_expression_1(p):
    '''
    add_expression : mult_expression
    '''
    p[0] = p[1]

def p_add_expression_2(p):
    '''
    add_expression : add_expression PLUS mult_expression
                   | add_expression MINUS mult_expression
    '''
    p[0] = ASTNode('binary_expression', p[2], [ p[1], p[3] ])

def p_mult_expression_1(p):
    '''
    mult_expression : exp_expression
    '''
    p[0] = p[1]

def p_mult_expression_2(p):
    '''
    mult_expression : mult_expression TIMES exp_expression
                    | mult_expression DIVIDE exp_expression
    '''
    p[0] = ASTNode('binary_expression', p[2], [ p[1], p[3] ])

def p_mult_expression_3(p):
    '''
    mult_expression : mult_expression exp_expression
    '''
    p[0] = ASTNode('binary_expression', '*', [ p[1], p[2] ])

def p_exp_expression_1(p):
    '''
    exp_expression : unary_expression
    '''
    p[0] = p[1]

def p_exp_expression_2(p):
    '''
    exp_expression : exp_expression POWER unary_expression
    '''
    p[0] = ASTNode('exp_expression', p[2], [ p[1], p[3] ])

def p_unary_expression_1(p):
    '''
    unary_expression : paren_expression
    '''
    p[0] = p[1]

def p_unary_expression_2(p):
    '''
    unary_expression : MINUS variable
    '''
    p[0] = ASTNode('unary_expression', p[1], [ p[2] ])

def p_paren_expression_1(p):
    '''
    paren_expression : variable
    '''
    p[0] = p[1]

def p_paren_expression_2(p):
    '''
    paren_expression : LPAREN add_expression RPAREN
    '''
    p[0] = p[2]

def p_variable_1(p):
    '''
    variable : constant
    '''
    p[0] = p[1]

def p_variable_2(p):
    '''
    variable : VARIABLE
    '''
    p[0] = ASTNode('variable', p[1])


def p_constant(p):
    '''
    constant : NUMBER
    '''
    p[0] = ASTNode('number', p[1])

def p_error(p):
    print 'Error!'

lex = lexer.lexer
parser = yacc.yacc()

def parse_string(data):
    return parser.parse(data)
