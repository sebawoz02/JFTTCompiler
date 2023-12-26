import algorithms


class CodeGenerator:
    def __init__(self, out):
        self.line = 0
        self.code_file = open(out, 'w')
        self.block_level = 0
        self.block_buffer = []

    def write(self, string):
        if self.block_level != 0:
            self.block_buffer[self.block_level - 1].append(string)
        else:
            self.code_file.write(string)
        self.line += 1

    def close(self):
        self.write("HALT\n")
        self.code_file.close()

    def inc_block_level(self):
        self.block_level += 1
        self.block_buffer.append([])

    def flush_block_buffer(self, line_num):
        # JPOS/JZERO line_num
        self.block_level -= 1
        self.block_buffer[self.block_level][0] += f'{line_num}\n'
        if self.block_level == 0:
            for line in self.block_buffer[0]:
                self.code_file.write(line)
        else:
            # Merge nested block
            for line in self.block_buffer[self.block_level]:
                self.block_buffer[self.block_level - 1].append(line)
        self.block_buffer.pop()

    def get_number_in_register(self, number, register):
        self.write(f"RST {register}\n")
        lines = 1
        if number != 0:
            self.write(f"INC {register}\n")
            lines += 1
            operations = algorithms.reach_target_number(number)
            for operation in operations:
                self.write(operation + f" {register}\n")
                lines += 1
        return lines

    """
    ASSIGN
    """

    # PIDENTIFIER ASSIGN NUM
    # save the number at a given index in memory
    # Returns number of lines written
    def assign_number(self, num, idx):
        # Get expected number in register a
        lines = self.get_number_in_register(num, 'a')
        # Save it in memory
        return lines + self.store(idx)

    # PIDENTIFIER ASSIGN pidentifier
    # save/copy the number from one index in memory under the other
    # Returns number of lines written
    def assign_identifier(self, idx1, idx2):
        lines = self.get_number_in_register(idx2, 'h')
        self.write("LOAD h\n")
        return lines + 1 + self.store(idx1)

    # STORE
    # save value from register 'a' at given idx in memory
    # Returns number of lines written
    def store(self, idx):
        lines = self.get_number_in_register(idx, 'h')
        self.write("STORE h\n")
        return lines + 1

    """
    OTHER COMMANDS
    """

    def command_write(self, value):
        # value = [idx/number, 'NUM'/'PIDENTIFIER'/'EXPRESSION', lines_of_code]
        lines = 0
        if value[1] == 'NUM':
            lines += self.get_number_in_register(value[0], 'a')
        elif value[1] == 'PIDENTIFIER':
            lines += self.get_number_in_register(value[0], 'h')
            self.write('LOAD h\n')
            lines += 1
        # if value[1] == 'EXPRESSION' its already in register a
        self.write('WRITE\n')
        return lines + 1

    def command_read(self, idx):
        self.write("READ\n")
        lines = self.get_number_in_register(idx, 'h')
        self.write("STORE h\n")
        return lines + 2

    """
    ARITHMETICAL OPERATIONS
    """

    def add_sub(self, value1, value2, mode='add') -> (None, str, int):
        if value1[1] == 'NUM' and value2[1] == 'NUM':
            return value1[0] + value2[0], 'NUM', 0
        lines = 0
        if value2[1] == 'PIDENTIFIER':
            lines += self.get_number_in_register(value2[0], 'h')
            self.write("LOAD h\n")
            self.write("PUT b\n")
            lines += 2
        else:
            lines += self.get_number_in_register(value2[0], 'b')
        if value1[1] == 'PIDENTIFIER':
            lines += self.get_number_in_register(value1[0], 'h')
            self.write("LOAD h\n")
            lines += 1
        else:
            lines += self.get_number_in_register(value1[0], 'a')
        if mode == 'add':
            self.write("ADD b\n")
        else:
            self.write("SUB b\n")
        return None, 'EXPRESSION', lines + 1

    """
    LOGICAL OPERATIONS
    """

    def op_eq(self, value1, value2):
        # EQ - max(v1 - v2, 0) + max(v2 - v1, 0) == 0
        lines = self.add_sub(value1, value2, mode='sub')[2]
        self.write('PUT c\n')
        lines += self.add_sub(value2, value1, mode='sub')[2]
        self.write('ADD c\n')
        self.inc_block_level()
        self.write('JPOS ')
        return lines + 3

    def op_neq(self, value1, value2):
        # NEQ - max(v1 - v2, 0) + max(v2 - v1, 0) > 0
        lines = self.add_sub(value1, value2, mode='sub')[2]
        self.write('PUT c\n')
        lines += self.add_sub(value2, value1, mode='sub')[2]
        self.write('ADD c\n')
        self.inc_block_level()
        self.write('JZERO ')
        return lines + 3

    def op_gt(self, value1, value2):
        # GT - max(v1 - v2, 0) > 0
        lines = self.add_sub(value1, value2, mode='sub')[2]
        self.inc_block_level()
        self.write('JZERO ')
        return lines + 1

    def op_lt(self, value1, value2):
        # LT - max(v2 - v1, 0) > 0
        lines = self.add_sub(value2, value1, mode='sub')[2]
        self.inc_block_level()
        self.write('JZERO ')
        return lines + 1

    def op_geq(self, value1, value2):
        # GEQ - max(v2 - v1, 0) == 0
        lines = self.add_sub(value2, value1, mode='sub')[2]
        self.inc_block_level()
        self.write('JPOS ')
        return lines + 1

    def op_leq(self, value1, value2):
        # LEQ - max(v1 - v2, 0) == 0
        lines = self.add_sub(value1, value2, mode='sub')[2]
        self.inc_block_level()
        self.write('JPOS ')
        return lines + 1
