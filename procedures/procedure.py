from value import ValInfo
import copy


class GenStep:
    """
    A class that is a function/step on the way to generating a complete procedure
    """

    def __init__(self, func, params, optional):
        self.func = func
        self.params = params
        self.optional = optional

    """
    A monstrous function with a simple purpose. 
    Replace all prepared parameters with their addresses and run the function.
    """

    def execute(self, params_dict: dict) -> int | ValInfo:
        par = copy.copy(self.params)

        for i in range(len(par)):
            if isinstance(par[i], list):
                for j in range(len(par[i])):
                    if isinstance(par[i][j], list):
                        for k in range(len(par[i][j])):
                            if par[i][j][k] in params_dict.keys():
                                par[i][j][k] = params_dict[par[i][j][k]]["idx"]

                    elif isinstance(par[i][j], dict) and par[i][j]["name"] in params_dict.keys():
                        par[i][j]["idx"] = params_dict[par[i][j]["name"]]["idx"]
                        if par[i][j]["type"] != params_dict[par[i][j]["name"]]["type"]:
                            print(f"\033[91mWrong type variable passed to procedure!\033[0m")
                            raise NameError
                        if self.optional is not None and self.optional[i][j] is not None:
                            par[i][j] += self.optional[i][j]

            elif isinstance(par[i], ValInfo):
                if isinstance(par[i].value, list):
                    for j in range(len(par[i].value)):
                        if par[i].value[j] in params_dict.keys():
                            par[i].value[j] = params_dict[par[i].value[j]]["idx"]
                            if self.optional is not None and self.optional[i][0][j] is not None:
                                par[i].value += self.optional[i][0][j]
                else:
                    if par[i].value in params_dict.keys():
                        par[i].value = params_dict[par[i].value]["idx"]
                        if self.optional is not None and self.optional[i][0] is not None:
                            par[i].value += self.optional[i][0]

            elif par[i] in params_dict.keys():
                par[i] = params_dict[par[i]]["idx"]
                if self.optional is not None and self.optional[i] is not None:
                    par[i] += self.optional[i]
        return self.func(*par)


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
        if no_bytes == 0 and address != -1:
            print(f"\033[91mCannot initialize array with size 0!\033[0m")
            raise NameError
        t = "1"
        s = False
        if identifier[0] == "T":
            identifier = identifier[1:]
            t = "T"
            no_bytes = -1
        elif no_bytes > 1:
            t = "T"
            s = [False] * no_bytes
        self.params[identifier] = {
            "name": identifier,
            "idx": address,
            "set": s,
            "type": t,
            "size": no_bytes,
        }
        if address == -1:
            self.head_declared_params.append(identifier)
        else:
            allocator.cur_idx += no_bytes

    def _fix_params(self, params):
        if len(params) != len(self.head_declared_params):
            print(f"\033[91mNot enough params in procedure call!\033[0m")
            raise NameError

        for i in range(len(params)):
            self.params[self.head_declared_params[i]]["idx"] = params[i]["idx"]
            self.params[self.head_declared_params[i]]["set"] = params[i]["set"]
            if self.params[self.head_declared_params[i]]["type"] != params[i]["type"]:
                print(f"\033[91mWrong type variable passed to procedure!\033[0m")
                raise NameError

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

        def case_begins(bl, fl, ife, wh, prev):
            fl.append(0)
            ife.append(0)
            wh.append(prev)
            return bl + 1

        for i in range(len(self.gen_steps)):
            step = self.gen_steps[i]
            if isinstance(step, str):
                match step:
                    case "ELSE_BEGINS":
                        if_else_fix_idx[block_level - 1] = fixup_lines[block_level - 1]
                    case "IF_ELSE_BEGINS":
                        block_level = case_begins(
                            block_level,
                            fixup_lines,
                            if_else_fix_idx,
                            while_fix_idx,
                            prev_len,
                        )
                    case "IF_ELSE_ENDS":
                        # Fix params
                        block_level -= 1
                        self.gen_steps[i + 1].params = [
                            if_else_fix_idx[block_level] + 1,
                            f"JUMP {cg.line}\n",
                        ]
                        self.gen_steps[i + 2].params = [
                            if_else_fix_idx[block_level] + 1
                        ]
                        self.gen_steps[i + 3].params = [
                            cg.line
                            - (fixup_lines[block_level] - if_else_fix_idx[block_level])
                            + 1
                        ]
                        fixup_lines.pop()
                        if_else_fix_idx.pop()
                    case "IF_BEGINS":
                        block_level = case_begins(
                            block_level,
                            fixup_lines,
                            if_else_fix_idx,
                            while_fix_idx,
                            prev_len,
                        )
                    case "IF_ENDS":
                        block_level -= 1
                        self.gen_steps[i + 1].params = [cg.line]
                        fixup_lines.pop()
                    case "WHILE_BEGINS":
                        block_level = case_begins(
                            block_level,
                            fixup_lines,
                            if_else_fix_idx,
                            while_fix_idx,
                            prev_len,
                        )
                    case "WHILE_ENDS":
                        block_level -= 1
                        self.gen_steps[i + 1].params = [cg.line + 1]
                        self.gen_steps[i + 2].params = [
                            f"JUMP {cg.line - fixup_lines[block_level] - while_fix_idx[block_level]}\n"
                        ]
                        fixup_lines.pop()
                    case "REPEAT_BEGINS":
                        block_level = case_begins(
                            block_level,
                            fixup_lines,
                            if_else_fix_idx,
                            while_fix_idx,
                            prev_len,
                        )
                    case "REPEAT_ENDS":
                        block_level -= 1
                        self.gen_steps[i + 1].params = [
                            cg.line - fixup_lines[block_level]
                        ]
                        fixup_lines.pop()

            else:
                k = step.execute(self.params)
                if k is None:
                    continue
                if isinstance(k, ValInfo):
                    if block_level > 0:
                        for j in range(block_level):
                            fixup_lines[j] += k.lines
                    total_lines += k.lines
                    prev_len = k.lines
                else:
                    if block_level > 0:
                        for j in range(block_level):
                            fixup_lines[j] += k
                    total_lines += k
                    prev_len = k
        return total_lines
