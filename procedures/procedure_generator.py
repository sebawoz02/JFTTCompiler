from procedures.procedure import Procedure


class ProcedureGenerator:
    def __init__(self):
        self.procedures_dict = {}
        self.current_procedure_name = ''
        self.definition = False

    def declare_new_procedure(self, allocator, name, params):
        if name in self.procedures_dict.keys():
            print(f"\033[91mProcedure with name '{name}' already declared!\033[0m")
            raise NameError
        self.procedures_dict[name] = Procedure(name)
        self.definition = True
        self.current_procedure_name = name
        for p in params:
            self.add_param(allocator, p, 0)

    def add_param(self, allocator, identifier, no_bytes, address=-1):
        self.procedures_dict[self.current_procedure_name].add_param(allocator, identifier, no_bytes, address)

    def add_step(self, func, params, optional):
        self.procedures_dict[self.current_procedure_name].add_step(func, params, optional)

    def insert_fixup_info(self, idx, info):
        self.procedures_dict[self.current_procedure_name].insert_fixup_info(idx, info)

    def get_curr_step_idx(self):
        return self.procedures_dict[self.current_procedure_name].get_curr_step_idx()

    "ARITHMETIC / LOGIC"
    def add_func_with_two_values(self, func, p):
        opt = [[p[0][0][1], None], [p[2][0][1], None]]
        self.add_step(func, [[p[0][0][0], p[0][1]], [p[2][0][0], p[2][1]]], opt)
        return 1

    "I/O"
    def add_io(self, func, p):
        if p[1][1] != 'AKU':
            self.add_step(func, [[p[1][0][0], p[1][1]]], [[p[1][0][1], None]])
        else:
            self.add_step(func, [[[p[1][0][0], p[1][0][1]], p[1][1]]], [[None, None]])
        return 1

    """
    Execute all generate steps
    """
    def generate_procedure(self, cg, name, params):
        if name not in self.procedures_dict.keys():
            print(f"\033[91mUse of undeclared procedure '{name}'!\033[0m")
            raise NameError
        p: Procedure = self.procedures_dict[name]
        return p.generate(cg, params)

    """
    Add all steps needed to generate assign inside procedure
    """
    def add_assign_step(self, cg, identifier, expression):
        steps = 0
        if identifier[1] == 'AKU':
            if expression[1] == 'EXPRESSION':
                steps += 1
                self.add_step(cg.write, ["PUT c\n"], [None])
            steps += 1
            self.add_step(cg.load_aku_idx, [identifier[0][0], identifier[0][1]], [None, None])
            if expression[1] == 'EXPRESSION':
                self.add_step(cg.write, ["PUT b\n"], [None])
                self.add_step(cg.write, ["GET c\n"], [None])
                self.add_step(cg.write, ["STORE b\n"], [None])
                return steps + 3
            else:
                self.add_step(cg.write, ["PUT c\n"], [None])
                steps += 1
            if expression[1] == 'NUM':
                self.add_step(cg.assign_number, [expression[0][0], identifier[0][0], True],
                              [expression[0][1], identifier[0][1], None])
            elif expression[1] == 'PIDENTIFIER':
                self.add_step(cg.assign_identifier, [identifier[0][0], expression[0][0], True],
                              [identifier[0][1], expression[0][1], None])
            else:
                self.add_step(cg.assign_aku, [identifier[0][0], expression[0][0], expression[0][1], True],
                              [identifier[0][1], None, None, None])
            return steps + 1
        else:
            if expression[1] == 'NUM':
                self.add_step(cg.assign_number, [expression[0][0], identifier[0][0]],
                              [expression[0][1], identifier[0][1]])
            elif expression[1] == 'PIDENTIFIER':
                self.add_step(cg.assign_identifier, [identifier[0][0], expression[0][0]],
                              [identifier[0][1], expression[0][1]])
            elif expression[1] == 'AKU':
                self.add_step(cg.assign_aku, [identifier[0][0], expression[0][0], expression[0][1]],
                              [identifier[0][1], None, None])
            else:
                self.add_step(cg.store, [identifier[0][0]], [identifier[0][1]])
            return steps + 1
