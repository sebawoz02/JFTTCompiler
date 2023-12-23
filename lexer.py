from sly import Lexer as SlyLex


class Lexer(SlyLex):
    tokens = {
        NUM, PIDENTIFIER,
        READ, WRITE,
        ASSIGN,
        NEQ, GEQ, LEQ, EQ, GT, LT,
        ENDIF, IF, THEN, ELSE,
        REPEAT, UNTIL,
        ENDWHILE, WHILE, DO,
        PROGRAM, PROCEDURE, IS, IN, END
    }

    literals = {
        '(', ')', '[', ']',
        ';', ',',
        'T',
        '+', '-', '*', '/', '%'
    }

    PIDENTIFIER = r'[_a-z]+'
    NUM = r'\d+'
    READ = r'READ'
    WRITE = r'WRITE'
    ASSIGN = r':='
    NEQ = r'!='
    LEQ = r'<='
    GEQ = r'>='
    EQ = r'='
    GT = r'>'
    LT = r'<'
    ENDIF = r'ENDIF'
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    REPEAT = r'REPEAT'
    UNTIL = r'UNTIL'
    ENDWHILE = r'ENDWHILE'
    WHILE = r'WHILE'
    DO = r'DO'
    PROGRAM = r'PROGRAM'
    PROCEDURE = r'PROCEDURE'
    IS = r'IS'
    IN = r'IN'
    END = r'END'

    ignore = ' \t'

    @_(r'#.*')
    def ignore_comment(self, t):
        pass

    # Track newlines
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(f"\033[91mSyntax error: Illegal character '{t.value[0]}' at line {t.lineno}\033[0m")
        exit(1)
