import algorithms


class CodeGenerator:
    def __init__(self, out):
        self.line = 1
        self.code_file = open(out, 'w')

    def write(self, string):
        self.code_file.write(string)
        self.line += 1

    def close(self):
        self.write("HALT\n")
        self.code_file.close()

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
    ARITHMETICAL OPERATIONS
    """

    def add(self, value1, value2):
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
        self.write("ADD b\n")
        return None, 'EXPRESSION', lines + 1

