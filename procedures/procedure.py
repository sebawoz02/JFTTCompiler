class GenStep:
    def __init__(self, func, params, optional):
        self.func = func
        self.params = params
        self.optional = optional

    def execute(self, params_dict: dict):
        for i in range(len(self.params)):
            if isinstance(self.params[i], list):
                for j in range(len(self.params[i])):
                    if isinstance(self.params[i][j], list):
                        for k in range(len(self.params[i][j])):
                            if self.params[i][j][k] in params_dict.keys():
                                self.params[i][j][k] = params_dict[self.params[i][j][k]]
                    elif self.params[i][j] in params_dict.keys():
                        if self.optional[i][j] is not None:
                            self.params[i][j] = params_dict[self.params[i][j]] + self.optional[i][j]
                        else:
                            self.params[i][j] = params_dict[self.params[i][j]]
            elif self.params[i] in params_dict.keys():
                if self.optional[i] is not None:
                    self.params[i] = params_dict[self.params[i]] + self.optional[i]
                else:
                    self.params[i] = params_dict[self.params[i]]
        return self.func(*self.params)


class Procedure:
    def __init__(self, name):
        self.name = name
        self.params = {}
        self.head_declared_params = []
        self.gen_steps = []

    def add_param(self, allocator, identifier, no_bytes, address=-1):
        if identifier in self.params.keys():
            print(f"\033[91mDouble declaration of '{identifier}' in procedure '{self.name}'!\033[0m")
            raise NameError
        if allocator.cur_idx + no_bytes >= (1 << 62):
            print(f"\033[91mAllocation error. Out of memory!\033[0m")
            raise NameError
        self.params[identifier] = address
        if address == -1:
            self.head_declared_params.append(identifier)
        allocator.cur_idx += no_bytes

    def _fix_params(self, params):
        if len(params) != len(self.head_declared_params):
            print(f"\033[91mNot enough params in procedure call!\033[0m")
            raise NameError
        for i in range(len(params)):
            self.params[self.head_declared_params[i]] = params[i]

    def add_step(self, func, params, optional):
        self.gen_steps.append(GenStep(func, params, optional))

    def get_curr_step_idx(self):
        return len(self.gen_steps)

    def insert_fixup_info(self, idx, info):
        self.gen_steps.insert(idx, info)

    def generate(self, cg, params):
        self._fix_params(params)
        if_else_fix_idx = []
        while_fix_idx = []
        block_level = 0
        fixup_lines = []
        total_lines = 0
        prev_len = 0
        for i in range(len(self.gen_steps)):
            step = self.gen_steps[i]
            if isinstance(step, str):
                match step:
                    case 'ELSE_BEGINS':
                        if_else_fix_idx[block_level - 1] = fixup_lines[block_level - 1]
                    case 'IF_ELSE_BEGINS':
                        block_level += 1
                        fixup_lines.append(0)
                        if_else_fix_idx.append(0)
                    case 'IF_ELSE_ENDS':
                        # Fix params
                        block_level -= 1
                        self.gen_steps[i + 1].params = [if_else_fix_idx[block_level] + 1,
                                                        f"JUMP {cg.line}\n"]
                        self.gen_steps[i + 2].params = [if_else_fix_idx[block_level] + 1]
                        self.gen_steps[i + 3].params = \
                            [cg.line - (fixup_lines[block_level] - if_else_fix_idx[block_level]) + 1]
                        fixup_lines.pop()
                        if_else_fix_idx.pop()
                    case 'IF_BEGINS':
                        block_level += 1
                        fixup_lines.append(0)
                    case 'IF_ENDS':
                        block_level -= 1
                        self.gen_steps[i + 1].params = [cg.line]
                        fixup_lines.pop()
                    case 'WHILE_BEGINS':
                        block_level += 1
                        fixup_lines.append(0)
                        while_fix_idx.append(prev_len)
                    case 'WHILE_ENDS':
                        block_level -= 1
                        self.gen_steps[i + 1].params = [cg.line + 1]
                        self.gen_steps[i + 2].params = \
                            [f"JUMP {cg.line - fixup_lines[block_level] - while_fix_idx[block_level]}\n"]
                        fixup_lines.pop()
                    case 'REPEAT_BEGINS':
                        block_level += 1
                        fixup_lines.append(0)
                    case 'REPEAT_ENDS':
                        block_level -= 1
                        self.gen_steps[i + 1].params = [cg.line - fixup_lines[block_level]]
                        fixup_lines.pop()

            else:
                k = step.execute(self.params)
                if k is None:
                    continue
                if isinstance(k, tuple):
                    if block_level > 0:
                        for j in range(block_level):
                            fixup_lines[j] += k[2]
                    total_lines += k[2]
                    prev_len = k[2]
                else:
                    if block_level > 0:
                        for j in range(block_level):
                            fixup_lines[j] += k
                    total_lines += k
                    prev_len = k
        return total_lines