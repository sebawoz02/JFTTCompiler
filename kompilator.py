from lexer import Lexer
from parser import Parser
import argparse


# ex1 - OK
# ex2 - OK
# ex3 - OK
# ex4 - NOT OK, wychodzenie poza range przy mnożeniu??
# ex5 - OK
# ex6 - OK
# ex7 - OK
# ex8 - OK
# ex9 - OK
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

# Optional todo:
# - smarter registry management h

if __name__ == "__main__":
    arg_pars = argparse.ArgumentParser(
        description="JFTT Compiler 2023 Sebastian Woźniak"
    )
    arg_pars.add_argument("input_file", help="Input file")
    arg_pars.add_argument(
        "output_file", nargs="?", default=None, help="Output file (optional)"
    )
    arg_pars.add_argument(
        "--Wno-unset",
        action="store_true",
        help="Disable 'unset' warnings. (Errors still active)",
    )
    arg_pars.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Turn on debug info"
    )

    args = arg_pars.parse_args()
    warnings = []
    if not args.Wno_unset:
        warnings.append("unset")
    if args.debug:
        warnings.append("debug")
    out = "out.mr"
    if args.output_file:
        out = args.output_file
    src = args.input_file

    lex = Lexer()
    par = Parser(out, warnings)

    try:
        with open(src, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print(f"File '{src}' not found.")
        exit(1)

    tokens = lex.tokenize(code)
    par.parse(tokens)
    par.finish()
