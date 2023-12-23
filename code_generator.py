import algorithms


class CodeGenerator:
    def __init__(self, out):
        self.line = 1
        self.code_file = open(out, 'w')

    def assign(self, num):
        operations = algorithms.reach_target_number(num)
        self.code_file.write("RST a\n")
        for operation in operations:
            self.code_file.write(operation + " a\n")
        self.code_file.write("STORE h\n")

    def close(self):
        self.code_file.close()
