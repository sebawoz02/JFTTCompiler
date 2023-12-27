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
    def procedures(self, p):        # TODO: procedures
        pass

    @_('procedures PROCEDURE proc_head IS IN commands END')
    def procedures(self, p):        # TODO: procedures
        pass

    @_('')
    def procedures(self, p):        # TODO: procedures
        pass

    @_('PROGRAM IS declarations IN commands END')
    def main(self, p):
        print(p[4])

    @_('PROGRAM IS IN commands END')
    def main(self, p):
        print(p[3])

    @_('commands command')
    def commands(self, p):
        return p[0] + p[1]

    @_('command')
    def commands(self, p):
        return p[0]

    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        # p[2] = [idx, 'NUM'/'PIDENTIFIER'/'EXPRESSION', lines_of_code] or [(idx1, idx2), 'AKU', lines_of_code]
        if p[2][0] == 'expression':
            p[2] = p[2][1]
        if p[0][1] == 'AKU':
            lines = 0
            if p[2][1] == 'EXPRESSION':
                self.cg.write("PUT c\n")
                lines += 1
            lines += self.cg.load_aku_idx(p[0][0][0], p[0][0][1])
            if p[2][1] == 'EXPRESSION':
                self.cg.write("PUT b\n")
                self.cg.write("GET c\n")
                self.cg.write("STORE b\n")
                return lines + 3 + p[2][2]
            else:
                self.cg.write("PUT c\n")
                lines += 1
            if p[2][1] == 'NUM':
                return self.cg.assign_number(p[2][0], p[0][0], address_in_c=True) + lines
            elif p[2][1] == 'PIDENTIFIER':
                return self.cg.assign_identifier(p[0][0], p[2][0], address_in_c=True) + lines
            else:
                return self.cg.assign_aku(p[0][0], p[2][0][0], p[2][0][1], address_in_c=True) + lines
        else:
            if p[2][1] == 'NUM':
                return self.cg.assign_number(p[2][0], p[0][0])
            elif p[2][1] == 'PIDENTIFIER':
                return self.cg.assign_identifier(p[0][0], p[2][0])
            elif p[2][1] == 'AKU':
                return self.cg.assign_aku(p[0][0], p[2][0][0], p[2][0][1])
            else:
                return self.cg.store(p[0][0]) + p[2][2]

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):
        total_lines = self.cg.line
        self.cg.block_buffer[self.cg.block_level - 1].insert(p[3] + 1, f'JUMP {total_lines + 1}\n')
        self.cg.line += 1
        # fix jumps after ELSE
        self.cg.fix_else_jumps(p[3]+2)
        self.cg.flush_block_buffer(total_lines - p[5] + 1)
        return p[1] + p[3] + p[5] + 1

    @_('IF condition THEN commands ENDIF')
    def command(self, p):
        total_lines = self.cg.line
        self.cg.flush_block_buffer(total_lines + p[3] + 1)
        return p[1] + p[3]

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):
        total_lines = self.cg.line
        self.cg.flush_block_buffer(total_lines + 1)
        self.cg.write(f'JUMP {total_lines - p[1] - p[3]}\n')
        return p[1] + p[3] + 1

    @_('REPEAT commands UNTIL condition ";"')
    def command(self, p):
        self.cg.flush_block_buffer(self.cg.line - p[1] - p[3])
        return p[1] + p[3]

    @_('proc_call ";"')     # TODO: procedures
    def command(self, p):
        pass

    @_('READ identifier ";"')
    def command(self, p):
        return self.cg.command_read(p[1])

    @_('WRITE value ";"')
    def command(self, p):
        return self.cg.command_write(p[1])

    @_('PIDENTIFIER "(" args_decl ")"')
    def proc_head(self, p):     # TODO: procedures
        pass

    @_('PIDENTIFIER "(" args ")"')
    def proc_call(self, p):     # TODO: procedures
        pass

    @_('declarations "," PIDENTIFIER')
    def declarations(self, p):
        self.EXCEPTION_WRAPPER(NameError, self.data.allocate, 1, p.PIDENTIFIER)

    @_('declarations "," PIDENTIFIER "[" NUM "]"')
    def declarations(self, p):
        self.EXCEPTION_WRAPPER(NameError, self.data.allocate, int(p.NUM), p.PIDENTIFIER)

    @_('PIDENTIFIER')
    def declarations(self, p):
        self.EXCEPTION_WRAPPER(NameError, self.data.allocate, 1, p.PIDENTIFIER)

    @_('PIDENTIFIER "[" NUM "]"')
    def declarations(self, p):
        self.EXCEPTION_WRAPPER(NameError, self.data.allocate, int(p.NUM), p.PIDENTIFIER)

    @_('args_decl "," PIDENTIFIER')
    def args_decl(self, p):     # TODO: procedures
        pass

    @_('args_decl "," "T" PIDENTIFIER')
    def args_decl(self, p):     # TODO: procedures
        pass

    @_('PIDENTIFIER')
    def args_decl(self, p):     # TODO: procedures
        pass

    @_('"T" PIDENTIFIER')
    def args_decl(self, p):     # TODO: procedures
        pass

    @_('args "," PIDENTIFIER')
    def args(self, p):          # TODO: procedures
        pass

    @_('PIDENTIFIER')
    def args(self, p):          # TODO: procedures
        pass

    @_('value')
    def expression(self, p):
        return p

    @_('value "+" value')
    def expression(self, p):
        return self.cg.add_sub(p[0], p[2])

    @_('value "-" value')
    def expression(self, p):
        return self.cg.add_sub(p[0], p[2], mode='sub')

    @_('value "*" value')
    def expression(self, p):
        return self.cg.multiply(p[0], p[2])

    @_('value "/" value')
    def expression(self, p):    # TODO: div
        return self.cg.divide(p[0], p[2])

    @_('value "%" value')
    def expression(self, p):    # TODO: div
        return self.cg.divide(p[0], p[2], mode='modulo')

    @_('value EQ value')
    def condition(self, p):
        lines = self.cg.op_eq(p[0], p[2])
        return lines

    @_('value NEQ value')
    def condition(self, p):
        lines = self.cg.op_neq(p[0], p[2])
        return lines

    @_('value GT value')
    def condition(self, p):
        lines = self.cg.op_gt(p[0], p[2])
        return lines

    @_('value LT value')
    def condition(self, p):
        lines = self.cg.op_lt(p[0], p[2])
        return lines

    @_('value GEQ value')
    def condition(self, p):
        lines = self.cg.op_geq(p[0], p[2])
        return lines

    @_('value LEQ value')
    def condition(self, p):
        lines = self.cg.op_leq(p[0], p[2])
        return lines

    @_('NUM')
    def value(self, p):
        return int(p.NUM), 'NUM', 0

    @_('identifier')
    def value(self, p):
        return p[0]

    @_('PIDENTIFIER')
    def identifier(self, p):
        return self.EXCEPTION_WRAPPER(NameError, self.data.get_index, p.PIDENTIFIER), 'PIDENTIFIER', 0

    @_('PIDENTIFIER "[" NUM "]"')
    def identifier(self, p):
        return self.EXCEPTION_WRAPPER(NameError, self.data.get_index, p.PIDENTIFIER) + int(p.NUM), 'PIDENTIFIER', 0

    @_('PIDENTIFIER "[" PIDENTIFIER "]"')
    def identifier(self, p):
        return (self.EXCEPTION_WRAPPER(NameError, self.data.get_index, p[0]),
                self.EXCEPTION_WRAPPER(NameError, self.data.get_index, p[2])), 'AKU', 0
