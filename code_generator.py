from code_generator_functions import arithmetic, assign, blocks, io, logical


# Calculates the quickest way from 1 to x using only SHL, INC or DEC
def reach_target_number(x, y=0):
    operations = []
    while x != 1:
        if x == y:
            return operations[::-1], x

        if x % 2 == 0:
            x //= 2
            operations.append("SHL")
        elif (x - 1) % 4 == 0 or x == 3:
            x -= 1
            operations.append("INC")
        else:
            x += 1
            operations.append("DEC")
    return operations[::-1]


class CodeGenerator:
    """
    The class responsible for generating code for the output file.
    """

    def __init__(self, out):
        self.line = 0
        self.code_file = open(out, 'w')
        self.block_level = 0
        self.block_buffer = []
        # registers used to store/load
        self.h_register = 0
        self.g_register = 0
        self.last_used_address_register = ""

    def write(self, string):
        if self.block_level != 0:
            self.block_buffer[self.block_level - 1].append(string)
        else:
            self.code_file.write(string)
        self.line += 1
        return 1

    def close(self):
        self.write("HALT\n")
        self.code_file.close()

    def get_number_in_register(self, number, register):
        if register == 'address':     # LOAD/STORE
            if number == 0:     # reset one of the registers
                if self.h_register > self.g_register:
                    self.write("RST g\n")
                    self.last_used_address_register = 'g'
                    self.g_register = 0
                else:
                    self.write("RST h\n")
                    self.last_used_address_register = 'h'
                    self.h_register = 0
                return 1

            # else check if h->number is quicker or g->number
            register, path = self.pick_better_register(number, self.h_register, self.g_register)
            self.last_used_address_register = register
            lines = 0
            if not isinstance(path, tuple):
                self.write(f"RST {register}\n")
                self.write(f"INC {register}\n")
                lines += 2
            else:
                path = path[0]
            for operation in path:
                self.write(operation + f" {register}\n")
                lines += 1
            return lines

        self.write(f"RST {register}\n")
        lines = 1
        if number != 0:
            self.write(f"INC {register}\n")
            lines += 1
            operations = reach_target_number(number)
            for operation in operations:
                self.write(operation + f" {register}\n")
                lines += 1
        return lines

    def pick_better_register(self, number, h, g):
        ph = reach_target_number(number, h)
        pg = reach_target_number(number, g)
        if isinstance(ph, tuple):
            ph_len = len(ph[0])
        else:
            ph_len = len(ph) + 2
        if isinstance(pg, tuple):
            pg_len = len(pg[0])
        else:
            pg_len = len(pg) + 2
        if pg_len > ph_len:
            self.h_register = number
            return 'h', ph
        else:
            self.g_register = number
            return 'g', pg

    """
    ASSIGN
    """

    def generate_assign(self, identifier, expression):
        return assign.generate_assign(self, identifier, expression)

    def assign_number(self, num, idx, address_in_c=False):
        return assign.assign_number(self, num, idx, address_in_c)

    def assign_identifier(self, idx1, idx2, address_in_c=False):
        return assign.assign_identifier(self, idx1, idx2, address_in_c)

    def assign_aku(self, idx1, idx2, idx3, address_in_c=False):
        return assign.assign_aku(self, idx1, idx2, idx3, address_in_c)

    def store(self, idx):
        return assign.store(self, idx)

    def load_aku_idx(self, idx1, idx2):
        return assign.load_aku_idx(self, idx1, idx2)

    """
    I/O COMMANDS
    """

    def command_write(self, value):
        return io.command_write(self, value)

    def command_read(self, value):
        return io.command_read(self, value)

    """
    ARITHMETICAL OPERATIONS
    """

    def add_sub(self, value1, value2, mode='add') -> (None, str, int):
        return arithmetic.add_sub(self, value1, value2, mode)

    def multiply(self, value1, value2) -> (None, str, int):
        return arithmetic.multiply(self, value1, value2)

    def divide(self, value1, value2, mode='div') -> (None, str, int):
        return arithmetic.divide(self, value1, value2, mode)

    """
    LOGICAL OPERATIONS
    """

    def op_eq(self, value1, value2):
        return logical.op_eq(self, value1, value2)

    def op_neq(self, value1, value2):
        return logical.op_neq(self, value1, value2)

    def op_gt(self, value1, value2):
        return logical.op_gt(self, value1, value2)

    def op_lt(self, value1, value2):
        return logical.op_lt(self, value1, value2)

    def op_geq(self, value1, value2):
        return logical.op_geq(self, value1, value2)

    def op_leq(self, value1, value2):
        return logical.op_leq(self, value1, value2)

    """
    IF, IF_ELSE, WHILE, REPEAT
    """

    def inc_block_level(self):
        self.block_level += 1
        self.block_buffer.append([])

    def block_buffer_insert(self, idx, string):
        self.block_buffer[self.block_level - 1].insert(idx, string)
        self.line += 1
        return 1

    def flush_block_buffer(self, line_num):
        blocks.flush_block_buffer(self, line_num)

    def fix_else_jumps(self, idx):
        blocks.fix_else_jumps(self, idx)
