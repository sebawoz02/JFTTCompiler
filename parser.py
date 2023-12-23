from sly import Parser as SlyPar
from lexer import Lexer
from code_generator import CodeGenerator
from data import Data


class Parser(SlyPar):

    tokens = Lexer.tokens

    def __init__(self, out):
        super().__init__()
        self.cg = CodeGenerator(out)
        self.data = Data()
        self.error = False

    def finish(self):
        self.cg.close()
        if self.error:
            print("Compilation failed!")
        else:
            print("Compilation completed successfully!")

    @_('procedures main')
    def program_all(self, p):
        pass

    @_('procedures PROCEDURE proc_head IS declarations IN commands END')
    def procedures(self, p):
        pass

    @_('procedures PROCEDURE proc_head IS IN commands END')
    def procedures(self, p):
        pass

    @_('')
    def procedures(self, p):
        pass

    @_('PROGRAM IS declarations IN commands END')
    def main(self, p):
        pass

    @_('PROGRAM IS IN commands END')
    def main(self, p):
        pass

    @_('commands command')
    def commands(self, p):
        pass

    @_('command')
    def commands(self, p):
        pass

    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        if p.expression[1][1] == 'NUM':
            self.cg.assign_number(p.expression[1][0], p.identifier)
        elif p.expression[1][1] == 'PIDENTIFIER':
            self.cg.assign_identifier(p.expression[1][0], p.identifier)

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        pass

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        pass

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        pass

    @_('REPEAT commands UNTIL condition ";"')
    def command(self, p):
        pass

    @_('proc_call ";"')
    def command(self, p):
        pass

    @_('READ identifier ";"')
    def command(self, p):
        pass

    @_('WRITE value ";"')
    def command(self, p):
        pass

    @_('PIDENTIFIER "(" args_decl ")"')
    def proc_head(self, p):
        pass

    @_('PIDENTIFIER "(" args ")"')
    def proc_call(self, p):
        pass

    @_('declarations "," PIDENTIFIER')
    def declarations(self, p):
        try:
            self.data.allocate(1, p.PIDENTIFIER)
        except NameError:
            self.error = True

    @_('declarations "," PIDENTIFIER "[" NUM "]"')
    def declarations(self, p):
        try:
            self.data.allocate(p.NUM, p.PIDENTIFIER)
        except NameError:
            self.error = True

    @_('PIDENTIFIER')
    def declarations(self, p):
        try:
            self.data.allocate(1, p.PIDENTIFIER)
        except NameError:
            self.error = True

    @_('PIDENTIFIER "[" NUM "]"')
    def declarations(self, p):
        try:
            self.data.allocate(p.NUM, p.PIDENTIFIER)
        except NameError:
            self.error = True

    @_('args_decl "," PIDENTIFIER')
    def args_decl(self, p):
        pass

    @_('args_decl "," "T" PIDENTIFIER')
    def args_decl(self, p):
        pass

    @_('PIDENTIFIER')
    def args_decl(self, p):
        pass

    @_('"T" PIDENTIFIER')
    def args_decl(self, p):
        pass

    @_('args "," PIDENTIFIER')
    def args(self, p):
        pass

    @_('PIDENTIFIER')
    def args(self, p):
        pass

    @_('value')
    def expression(self, p):
        return p

    @_('value "+" value')
    def expression(self, p):
        pass

    @_('value "-" value')
    def expression(self, p):
        pass

    @_('value "*" value')
    def expression(self, p):
        pass

    @_('value "/" value')
    def expression(self, p):
        pass

    @_('value "%" value')
    def expression(self, p):
        pass

    @_('value EQ value')
    def condition(self, p):
        pass

    @_('value NEQ value')
    def condition(self, p):
        pass

    @_('value GT value')
    def condition(self, p):
        pass

    @_('value LT value')
    def condition(self, p):
        pass

    @_('value GEQ value')
    def condition(self, p):
        pass

    @_('value LEQ value')
    def condition(self, p):
        pass

    @_('NUM')
    def value(self, p):
        return int(p.NUM), 'NUM'

    @_('identifier')
    def value(self, p):
        return p.identifier, 'PIDENTIFIER'

    @_('PIDENTIFIER')
    def identifier(self, p):
        try:
            return self.data.get_index(p.PIDENTIFIER)
        except NameError:
            self.error = True

    @_('PIDENTIFIER "[" NUM "]"')
    def identifier(self, p):
        try:
            return self.data.get_index(p.PIDENTIFIER) + int(p.NUM)
        except NameError:
            self.error = True

    @_('PIDENTIFIER "[" PIDENTIFIER "]"')
    def identifier(self, p):
        try:
            return self.data.get_index(p[0]) + self.data.get_index(p[2])
        except NameError:
            self.error = True
