from value import ValInfo


class Allocator:
    """
    The class manages the assignment of memory addresses for variables
    """

    def __init__(self):
        self.variable_indexes = {}
        self.cur_idx = 0

    def allocate(self, no_bytes, identifier):
        if identifier in self.variable_indexes.keys():
            print(f"\033[91mDouble declaration of '{identifier}'!\033[0m")
            raise NameError
        if self.cur_idx >= (1 << 62):
            print(f"\033[91mAllocation error. Out of memory!\033[0m")
            raise NameError
        if no_bytes == 0:
            print(f"\033[91mCannot initialize array with size 0!\033[0m")
            raise NameError
        t = "1"
        s = False
        if no_bytes > 1:
            t = "T"
            s = [False] * no_bytes
        self.variable_indexes[identifier] = {"name": identifier, "idx": self.cur_idx, "set": s, "type": t}
        self.cur_idx += no_bytes

    def get_index(self, identifier):
        if identifier not in self.variable_indexes.keys():
            print(f"\033[91mUse of undeclared variable '{identifier}'!\033[0m")
            raise NameError
        return self.variable_indexes[identifier]["idx"]

    def get_type(self, identifier):
        if identifier not in self.variable_indexes.keys():
            print(f"\033[91mUse of undeclared variable '{identifier}'!\033[0m")
            raise NameError
        return self.variable_indexes[identifier]["type"]

    def is_set(self, identifier: ValInfo):
        if identifier.identifier not in self.variable_indexes.keys():
            print(f"\033[91mUse of undeclared variable '{identifier.identifier}'!\033[0m")
            raise NameError
        if identifier.idx != -1 and not self.variable_indexes[identifier.identifier]["set"]:
            return self.variable_indexes[identifier.identifier]["set"][identifier.idx]
        return self.variable_indexes[identifier.identifier]["set"]

    def get_info(self, identifier):
        if identifier not in self.variable_indexes.keys():
            print(f"\033[91mUse of undeclared variable '{identifier}'!\033[0m")
            raise NameError
        return self.variable_indexes[identifier]

    def set_variable(self, identifier: ValInfo):
        if identifier.identifier not in self.variable_indexes.keys():
            print(f"\033[91mUse of undeclared variable '{identifier}'!\033[0m")
            raise NameError
        if identifier.v_type == 'AKU':
            self.variable_indexes[identifier.identifier]["set"] = True
        elif identifier.idx != -1 and not self.variable_indexes[identifier.identifier]["set"]:
            self.variable_indexes[identifier.identifier]["set"][identifier.idx] = True
        else:
            self.variable_indexes[identifier.identifier]["set"] = True
