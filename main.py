from lexer import Lexer
from parser import Parser
import sys


# TODO 1: Passing arrays to procedures
# TODO 2: division/modulo
# TODO 3: error handling

# ex1 - brakuje dzielenia i modulo
# ex2 - OK
# ex3 - OK
# ex4 - brakuje modulo
# ex5 - brakuje modulo
# ex6 - OK
# ex7 - OK
# ex8 - brakuje modulo, brakuje T
# ex9 - brakuje dzielenia, brakuje T

# Oblugiwane błedy:
# - Double declaration (zmienna, procedura, zmienne w procedurze)
# - Out of memory
# - Syntax error ( parser, lexer )
# - Usage of undeclared variable ( program, TODO: procedure)
# - TODO: Usage of unset variable
# - TODO: Invalid type passed to procedure

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
