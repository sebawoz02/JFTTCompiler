from code_generator_functions import arithmetic, assign, blocks, io, logical


def reach_target_number(x, y=0):
    """
    Calculates the quickest way from 1 to x using only SHL, INC or DEC
    """
    operations = []
    while x != 1:
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
        self.code_file = open(out, "w")
        self.block_level = 0
        self.block_buffer = []

    def write(self, string):
        """
        Writes a string to the code file, either directly or by appending it to
        the block buffer if the block level is not zero.
        Increments the line counter.
        :param string: string to write
        :return: Returns 1 to indicate the success of write. ( num of lines written)
        """
        if self.block_level != 0:
            self.block_buffer[self.block_level - 1].append(string)
        else:
            self.code_file.write(string)
        self.line += 1
        return 1

    def close(self):
        """
        Writes a "HALT" instruction to the code file.
        Closes the code file.
        """
        self.write("HALT\n")
        self.code_file.close()

    def get_number_in_register(self, number, register):
        """
        Manages loading a number into a specified register.
        Handles both address and data registers.
        Utilizes the pick_better_register function to optimize register selection.
        :param number: number to get into register
        :param register: id or type
        :return:
        """
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

    def add_sub(self, value1, value2, mode="add") -> (None, str, int):
        return arithmetic.add_sub(self, value1, value2, mode)

    def multiply(self, value1, value2) -> (None, str, int):
        return arithmetic.multiply(self, value1, value2)

    def divide(self, value1, value2, mode="div") -> (None, str, int):
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
