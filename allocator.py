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
        self.variable_indexes[identifier] = self.cur_idx
        self.cur_idx += no_bytes

    def get_index(self, identifier):
        if identifier not in self.variable_indexes.keys():
            print(f"\033[91mUse of undeclared variable '{identifier}'!\033[0m")
            raise NameError
        return self.variable_indexes[identifier]
