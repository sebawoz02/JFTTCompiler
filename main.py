from lexer import Lexer
from parser import Parser
import sys

# TODO:
# - Passing arrays to procedures
# - check if variable is set when used
# - division/modulo

# ex1 - brakuje dzielenia i modulo
# ex2 - OK
# ex3 - OK
# ex4 - brakuje modulo
# ex5 - brakuje modulo
# ex6 - OK
# ex7 - OK
# ex8 - brakuje modulo
# ex9 - brakuje dzielenia

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
