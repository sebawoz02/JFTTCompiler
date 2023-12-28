from lexer import Lexer
from parser import Parser
import sys

# TODO:
# - Passing arrays to procedures
# - check if variable is set when used
# - division/modulo

if __name__ == '__main__':
    src = sys.argv[1]
    out = sys.argv[2]

    lex = Lexer()
    par = Parser(out)

    with open(src, 'r') as file:
        code = file.read()

    tokens = lex.tokenize(code)
    par.parse(tokens)
    par.finish()
