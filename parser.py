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

    def finish(self):
        self.cg.close()
        print("Compilation completed successfully!")

    def EXCEPTION_WRAPPER(self, ex, func, *args):
        try:
            return func(*args)
        except ex:
            self.cg.close()
            print("Compilation failed!")
            exit(1)

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
        # p = ('expression', [idx, 'NUM'/'PIDENTIFIER'/'EXPRESSION', lines_of_code]
        # or just
        # [idx, 'NUM'/'PIDENTIFIER'/'EXPRESSION', lines_of_code]
        if p.expression[1][1] == 'NUM':
            return self.cg.assign_number(p.expression[1][0], p.identifier)
        elif p.expression[1] == 'NUM':
            return self.cg.assign_number(p.expression[0], p.identifier)
        elif p.expression[1][1] == 'PIDENTIFIER':
            return self.cg.assign_identifier(p.expression[1][0], p.identifier)
        else:
            return self.cg.store(p.identifier) + p.expression[2]

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
        self.EXCEPTION_WRAPPER(NameError, self.data.allocate, 1, p.PIDENTIFIER)

    @_('declarations "," PIDENTIFIER "[" NUM "]"')
    def declarations(self, p):
        self.EXCEPTION_WRAPPER(NameError, self.data.allocate, p.NUM, p.PIDENTIFIER)

    @_('PIDENTIFIER')
    def declarations(self, p):
        self.EXCEPTION_WRAPPER(NameError, self.data.allocate, 1, p.PIDENTIFIER)

    @_('PIDENTIFIER "[" NUM "]"')
    def declarations(self, p):
        self.EXCEPTION_WRAPPER(NameError, self.data.allocate, p.NUM, p.PIDENTIFIER)

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
        return self.cg.add(p[0], p[2])

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
        return int(p.NUM), 'NUM', 0

    @_('identifier')
    def value(self, p):
        return p.identifier, 'PIDENTIFIER', 0

    @_('PIDENTIFIER')
    def identifier(self, p):
        return self.EXCEPTION_WRAPPER(NameError, self.data.get_index, p.PIDENTIFIER)

    @_('PIDENTIFIER "[" NUM "]"')
    def identifier(self, p):
        return self.EXCEPTION_WRAPPER(NameError, self.data.get_index, p.PIDENTIFIER) + int(p.NUM)

    @_('PIDENTIFIER "[" PIDENTIFIER "]"')
    def identifier(self, p):
        return (self.EXCEPTION_WRAPPER(NameError, self.data.get_index, p[0]) +
                self.EXCEPTION_WRAPPER(NameError, self.data.get_index, p[2]))
