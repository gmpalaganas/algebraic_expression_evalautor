import parser
from math import log

def interpret(ast,var_table=None):
    if ast.type == 'number':
        return int(ast.value)
    elif ast.type == 'variable':
        if not var_table.has_key(ast.value):
            if var_table:
                var_table[ast.value] = var_table.values()[-1] + 1
            else:
                var_table[ast.value] = 1
        return var_table[ast.value]
    elif ast.type == 'binary_expression':
        val1 = interpret(ast.children[0],var_table)
        val2 = interpret(ast.children[1],var_table)
        if ast.value == '+':
            return val1 + val2
        elif ast.value == '-':
            return val1 - val2
        elif ast.value == '*':
            return val1 * val2
        elif ast.value == '/':
            return val1 / val2
    elif ast.type == 'exp_expression':
        val1 = interpret(ast.children[0],var_table)
        val2 = interpret(ast.children[1],var_table)
        return val1 ** val2
    elif ast.type == 'equality_expression':
        val1 = interpret(ast.children[0],var_table)
        val2 = interpret(ast.children[1],var_table)
        return val1 == val2
    elif ast.type == 'unary_expression':
        val1 = interpret(ast.children[0],var_table)
        return -val1
    elif ast.type == 'log_expression':
        val1 = interpret(ast.children[0],var_table)
        return log(val1)
