from lexer import Lexer
import sys


if __name__ == '__main__':
    lex = Lexer()
    src = sys.argv[1]
    with open(src, 'r') as file:
        code = file.read()
        for token in lex.tokenize(code):
            print(token)
