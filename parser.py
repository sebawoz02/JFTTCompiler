from sly import Parser as SlyPar
from lexer import Lexer
from code_generator import CodeGenerator
from allocator import Allocator
from procedures.procedure_generator import ProcedureGenerator


class Parser(SlyPar):

    tokens = Lexer.tokens

    def __init__(self, out):
        super().__init__()
        self.cg = CodeGenerator(out)
        self.allocator = Allocator()
        self.pg = ProcedureGenerator()

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
        print(p[1])

    @_('procedures PROCEDURE proc_head IS declarations IN commands END')
    def procedures(self, p):
        self.pg.definition = False

    @_('procedures PROCEDURE proc_head IS IN commands END')
    def procedures(self, p):
        self.pg.definition = False

    @_('')
    def procedures(self, p):
        pass

    @_('PROGRAM IS declarations IN commands END')
    def main(self, p):
        return p[4]

    @_('PROGRAM IS IN commands END')
    def main(self, p):
        return p[3]

    @_('commands command')
    def commands(self, p):
        return p[0] + p[1]

    @_('command')
    def commands(self, p):
        return p[0]

    @_('identifier ASSIGN expression ";"')
    def command(self, p):
        if p[2][0] == 'expression':
            p[2] = p[2][1]

        if self.pg.definition:
            self.pg.add_assign_step(self.cg, p[0], p[2])
            return 0
        return self.cg.generate_assign(p[0], p[2])

    @_('IF condition THEN commands ELSE commands ENDIF')
    def command(self, p):          # TODO: procedures
        total_lines = self.cg.line
        self.cg.block_buffer[self.cg.block_level - 1].insert(p[3] + 1, f'JUMP {total_lines + 1}\n')
        self.cg.line += 1
        # fix jumps after ELSE
        self.cg.fix_else_jumps(p[3]+2)
        self.cg.flush_block_buffer(total_lines - p[5] + 1)
        return p[1] + p[3] + p[5] + 1

    @_('IF condition THEN commands ENDIF')
    def command(self, p):          # TODO: procedures
        total_lines = self.cg.line
        self.cg.flush_block_buffer(total_lines + p[3] + 1)
        return p[1] + p[3]

    @_('WHILE condition DO commands ENDWHILE')
    def command(self, p):          # TODO: procedures
        total_lines = self.cg.line
        self.cg.flush_block_buffer(total_lines + 1)
        self.cg.write(f'JUMP {total_lines - p[1] - p[3]}\n')
        return p[1] + p[3] + 1

    @_('REPEAT commands UNTIL condition ";"')
    def command(self, p):          # TODO: procedures
        self.cg.flush_block_buffer(self.cg.line - p[1] - p[3])
        return p[1] + p[3]

    @_('proc_call ";"')
    def command(self, p):
        return p[0]

    @_('READ identifier ";"')
    def command(self, p):
        if self.pg.definition:
            if p[1][1] != 'AKU':
                self.pg.add_step(self.cg.command_read, [[p[1][0][0], p[1][1]]], [p[1][0][1]])
            else:
                self.pg.add_step(self.cg.command_read, [[[p[1][0][0], p[1][0][1]], p[1][1]]], [None])
            return 0
        return self.cg.command_read(p[1])

    @_('WRITE value ";"')
    def command(self, p):
        if self.pg.definition:
            if p[1][1] != 'AKU':
                self.pg.add_step(self.cg.command_write, [[p[1][0][0], p[1][1]]], [p[1][0][1]])
            else:
                self.pg.add_step(self.cg.command_write, [[[p[1][0][0], p[1][0][1]], p[1][1]]], [None])
            return 0
        return self.cg.command_write(p[1])

    @_('PIDENTIFIER "(" args_decl ")"')
    def proc_head(self, p):
        self.EXCEPTION_WRAPPER(NameError, self.pg.declare_new_procedure, self.allocator, p[0], p[2])

    @_('PIDENTIFIER "(" args ")"')
    def proc_call(self, p):
        if self.pg.definition:
            self.pg.add_step(self.pg.generate_procedure, [p[0], p[2]], [None, None])
        return self.pg.generate_procedure(p[0], p[2])

    @_('declarations "," PIDENTIFIER')
    def declarations(self, p):
        if self.pg.definition:
            self.pg.add_param(self.allocator, p[2], 1, self.allocator.cur_idx)
            return
        self.EXCEPTION_WRAPPER(NameError, self.allocator.allocate, 1, p.PIDENTIFIER)

    @_('declarations "," PIDENTIFIER "[" NUM "]"')
    def declarations(self, p):
        if self.pg.definition:
            self.pg.add_param(self.allocator, p[2], int(p[4]), self.allocator.cur_idx)
            return
        self.EXCEPTION_WRAPPER(NameError, self.allocator.allocate, int(p.NUM), p.PIDENTIFIER)

    @_('PIDENTIFIER')
    def declarations(self, p):
        if self.pg.definition:
            self.pg.add_param(self.allocator, p[0], 1, self.allocator.cur_idx)
            return
        self.EXCEPTION_WRAPPER(NameError, self.allocator.allocate, 1, p.PIDENTIFIER)

    @_('PIDENTIFIER "[" NUM "]"')
    def declarations(self, p):
        if self.pg.definition:
            self.pg.add_param(self.allocator, p[0], int(p[2]), self.allocator.cur_idx)
            return
        self.EXCEPTION_WRAPPER(NameError, self.allocator.allocate, int(p.NUM), p.PIDENTIFIER)

    @_('args_decl "," PIDENTIFIER')
    def args_decl(self, p):
        return [*p[0], p[2]]

    @_('args_decl "," "T" PIDENTIFIER')
    def args_decl(self, p):     # TODO: T procedures
        return [*p[0], "T " + p[2]]

    @_('PIDENTIFIER')
    def args_decl(self, p):
        return [p[0]]

    @_('"T" PIDENTIFIER')
    def args_decl(self, p):     # TODO: T procedures
        return ["T " + p[0]]

    @_('args "," PIDENTIFIER')
    def args(self, p):
        return [*p[0], self.allocator.get_index(p[2])]

    @_('PIDENTIFIER')
    def args(self, p):
        return [self.allocator.get_index(p[0])]

    @_('value')
    def expression(self, p):
        return p

    @_('value "+" value')
    def expression(self, p):
        return self.cg.add_sub(p[0], p[2])          # TODO: procedures

    @_('value "-" value')
    def expression(self, p):
        return self.cg.add_sub(p[0], p[2], mode='sub')          # TODO: procedures

    @_('value "*" value')
    def expression(self, p):
        return self.cg.multiply(p[0], p[2])          # TODO: procedures

    @_('value "/" value')
    def expression(self, p):    # TODO: div          # TODO: procedures
        return self.cg.divide(p[0], p[2])

    @_('value "%" value')
    def expression(self, p):    # TODO: div          # TODO: procedures
        return self.cg.divide(p[0], p[2], mode='modulo')

    @_('value EQ value')
    def condition(self, p):
        lines = self.cg.op_eq(p[0], p[2])          # TODO: procedures
        return lines

    @_('value NEQ value')
    def condition(self, p):
        lines = self.cg.op_neq(p[0], p[2])          # TODO: procedures
        return lines

    @_('value GT value')
    def condition(self, p):
        lines = self.cg.op_gt(p[0], p[2])          # TODO: procedures
        return lines

    @_('value LT value')
    def condition(self, p):
        lines = self.cg.op_lt(p[0], p[2])          # TODO: procedures
        return lines

    @_('value GEQ value')
    def condition(self, p):
        lines = self.cg.op_geq(p[0], p[2])          # TODO: procedures
        return lines

    @_('value LEQ value')
    def condition(self, p):
        lines = self.cg.op_leq(p[0], p[2])          # TODO: procedures
        return lines

    @_('NUM')
    def value(self, p):
        if self.pg.definition:
            return (int(p[0]), None), 'NUM'
        return int(p.NUM), 'NUM', 0

    @_('identifier')
    def value(self, p):
        return p[0]

    @_('PIDENTIFIER')
    def identifier(self, p):
        if self.pg.definition:
            return (p[0], None), 'PIDENTIFIER'
        return self.EXCEPTION_WRAPPER(NameError, self.allocator.get_index, p.PIDENTIFIER), 'PIDENTIFIER', 0

    @_('PIDENTIFIER "[" NUM "]"')
    def identifier(self, p):
        if self.pg.definition:
            return (p[0], int(p[2])), 'PIDENTIFIER'
        return self.EXCEPTION_WRAPPER(NameError, self.allocator.get_index, p.PIDENTIFIER) + int(p.NUM), 'PIDENTIFIER', 0

    @_('PIDENTIFIER "[" PIDENTIFIER "]"')
    def identifier(self, p):
        if self.pg.definition:
            return (p[0], p[2]), 'AKU'
        return (self.EXCEPTION_WRAPPER(NameError, self.allocator.get_index, p[0]),
                self.EXCEPTION_WRAPPER(NameError, self.allocator.get_index, p[2])), 'AKU', 0
