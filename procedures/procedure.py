class GenStep:
    def __init__(self, func, params, optional):
        self.func = func
        self.params = params
        self.optional = optional

    def execute(self, params_dict: dict):
        for i in range(len(self.params)):
            if isinstance(self.params[i], list):
                for j in range(len(self.params[i])):
                    if self.params[i][j] in params_dict.keys():
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

    def generate(self, params):
        self._fix_params(params)
        lines = 0
        for step in self.gen_steps:
            lines += step.execute(self.params)
        return lines

