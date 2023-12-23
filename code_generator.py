import algorithms


class CodeGenerator:
    def __init__(self, out):
        self.line = 1
        self.code_file = open(out, 'w')

    # PIDENTIFIER ASSIGN NUM
    # save the number at a given index in memory
    def assign_number(self, num, idx):
        # Get expected number in register a
        self.code_file.write("RST a\n")
        if num != 0:
            self.code_file.write("INC a\n")
            operations = algorithms.reach_target_number(num)
            for operation in operations:
                self.code_file.write(operation + " a\n")
        # Save it in memory
        self.store(idx)

    # PIDENTIFIER ASSIGN pidentifier
    # save/copy the number from one index in memory under the other
    def assign_identifier(self, idx1, idx2):
        self.code_file.write("RST h\n")
        if idx2 != 0:
            self.code_file.write("INC h\n")
            operations = algorithms.reach_target_number(idx2)
            for operation in operations:
                self.code_file.write(operation + " h\n")
        self.code_file.write("LOAD h\n")
        self.store(idx1)

    # STORE
    # save value from register 'a' at given idx in memory
    def store(self, idx):
        self.code_file.write("RST h\n")
        if idx != 0:
            self.code_file.write("INC h\n")
            operations = algorithms.reach_target_number(idx)
            for operation in operations:
                self.code_file.write(operation + " h\n")
        self.code_file.write("STORE h\n")

    def close(self):
        self.code_file.write("HALT\n")
        self.code_file.close()
