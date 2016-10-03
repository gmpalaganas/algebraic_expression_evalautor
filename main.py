# Input an algebraic expression and evaluates it
# i.e. 3 + 5 returns 8
#      2x = x + x returns True
#      2x returns 2 (variables are assigned values 1 and increments for each unique variables)
#      2x + 2y returns 6
#      2(x + y) = 2x + 2y returns True
#
# Requires python-ply library for parsing input
# pip install ply

from parser import parse_string
from interpreter import interpret

def main():
    string = raw_input('Input string to be interpreted: ')
    ast = parse_string(string)
    f = open('ast_log.txt','w+')
    f.write(str(ast))
    var_table = {}
    print interpret(ast,var_table)
    f.close()


if __name__ == '__main__':
    main()
