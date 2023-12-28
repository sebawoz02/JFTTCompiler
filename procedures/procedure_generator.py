from procedures.procedure import Procedure
from value import ValInfo


class ProcedureGenerator:
    """
    This class stores declared procedures and generates arrays of steps needed to generate them.
    """
    def __init__(self):
        self.procedures_dict = {}
        self.current_procedure_name = ''
        self.definition = False     # if parsing should be done as for procedure, not for program

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
        p1: ValInfo = p[0]
        p2: ValInfo = p[2]
        opt = [[p1.value[1], None], [p2.value[1], None]]
        self.add_step(func, [ValInfo(p1.value[0], p1.v_type), ValInfo(p2.value[0], p2.v_type)], opt)
        return 1

    "I/O"
    def add_io(self, func, p: ValInfo):
        if p.v_type != 'AKU':
            self.add_step(func, [ValInfo(p.value[0], p.v_type)], [[p.value[1], None]])
        else:
            self.add_step(func, [ValInfo([p.value[0], p.value[1]], p.v_type)], [[None, None]])
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
    def add_assign_step(self, cg, identifier: ValInfo, expression: ValInfo):
        steps = 0
        if identifier.v_type == 'AKU':
            if expression.v_type == 'EXPRESSION':
                steps += 1
                self.add_step(cg.write, ["PUT c\n"], [None])
            steps += 1
            self.add_step(cg.load_aku_idx, [identifier.value[0], identifier.value[1]], [None, None])
            if expression.v_type == 'EXPRESSION':
                self.add_step(cg.write, ["PUT b\n"], [None])
                self.add_step(cg.write, ["GET c\n"], [None])
                self.add_step(cg.write, ["STORE b\n"], [None])
                return steps + 3
            else:
                self.add_step(cg.write, ["PUT c\n"], [None])
                steps += 1
            if expression.v_type == 'NUM':
                self.add_step(cg.assign_number, [expression.value[0], identifier.value[0], True],
                              [expression.value[1], identifier.value[1], None])
            elif expression.v_type == 'PIDENTIFIER':
                self.add_step(cg.assign_identifier, [identifier.value[0], expression.value[0], True],
                              [identifier.value[1], expression.value[1], None])
            else:
                self.add_step(cg.assign_aku, [identifier.value[0], expression.value[0], expression.value[1], True],
                              [identifier.value[1], None, None, None])
            return steps + 1
        else:
            if expression.v_type == 'NUM':
                self.add_step(cg.assign_number, [expression.value[0], identifier.value[0]],
                              [expression.value[1], identifier.value[1]])
            elif expression.v_type == 'PIDENTIFIER':
                self.add_step(cg.assign_identifier, [identifier.value[0], expression.value[0]],
                              [identifier.value[1], expression.value[1]])
            elif expression.v_type == 'AKU':
                self.add_step(cg.assign_aku, [identifier.value[0], expression.value[0], expression.value[1]],
                              [identifier.value[1], None, None])
            else:
                self.add_step(cg.store, [identifier.value[0]], [identifier.value[1]])
            return steps + 1
