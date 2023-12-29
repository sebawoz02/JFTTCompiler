from lexer import Lexer
from parser import Parser
import sys


# ex1 - OK
# ex2 - OK
# ex3 - OK
# ex4 - NOT OK, zły wynik
# ex5 - OK
# ex6 - OK
# ex7 - OK
# ex8 - OK
# ex9 - NOT OK, zły wynik
# ex10- OK

# Oblugiwane błedy:
# - Double declaration (zmienna, procedura, zmienne w procedurze)
# - Out of memory
# - Syntax error ( parser, lexer )
# - Usage of undeclared variable ( program, procedure)
# - Usage of unset variable
# - Invalid type passed to procedure
# - Index out of range
# - Double array -> a[b[1]]
# - Use of int as array/array as int

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
