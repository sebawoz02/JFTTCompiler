from value import ValInfo


class Allocator:
    """
    The class manages the assignment of memory addresses for variables
    """

    def __init__(self):
        self.variable_indexes = {}
        self.cur_idx = 0

    def allocate(self, no_bytes: int, identifier: str) -> None:
        """
        Allocates memory for a variable with a specified size and identifier.
        Checks for double declaration, out of memory, and zero-sized arrays.
        Sets up the variable in the internal data structure.
        :param no_bytes: bytes to allocate
        :param identifier: variable id
        :return: None
        """
        # Check for double declaration
        if identifier in self.variable_indexes.keys():
            print(f"\033[91mDouble declaration of '{identifier}'!\033[0m")
            raise NameError
        # Check for out of memory
        if self.cur_idx >= (1 << 62):
            print(f"\033[91mAllocation error. Out of memory!\033[0m")
            raise NameError
        # Check for zero-sized arrays
        if no_bytes == 0:
            print(f"\033[91mCannot initialize array with size 0!\033[0m")
            raise NameError
        # Initialize variable properties and update internal data structure
        t = "1"
        s = False
        if no_bytes > 1:
            t = "T"
            s = [False] * no_bytes
        self.variable_indexes[identifier] = {
            "name": identifier,
            "idx": self.cur_idx,
            "set": s,
            "type": t,
            "size": no_bytes,
        }
        self.cur_idx += no_bytes

    def get_index(self, identifier: str) -> int:
        """
        Retrieves index of a declared variable.

        :param identifier: id
        :return: index
        """
        # Check for undeclared variable
        if identifier not in self.variable_indexes.keys():
            print(f"\033[91mUse of undeclared variable '{identifier}'!\033[0m")
            raise NameError
        # Return the index of the variable
        return self.variable_indexes[identifier]["idx"]

    def get_type(self, identifier: str) -> str:
        """
        Retrieves the type of declared variable.
        :param identifier: id
        :return: type
        """
        # Check for undeclared variable
        if identifier not in self.variable_indexes.keys():
            print(f"\033[91mUse of undeclared variable '{identifier}'!\033[0m")
            raise NameError
        # Return the type of the variable
        return self.variable_indexes[identifier]["type"]

    def is_set(self, identifier: str | ValInfo) -> bool:
        """
        Checks if a variable or array element is set.
        :param identifier: id
        :return: bool
        """
        # Check if identifier is a string or an object
        if isinstance(identifier, str):
            # Check for undeclared variable
            if identifier not in self.variable_indexes.keys():
                print(f"\033[91mUse of undeclared variable '{identifier}'!\033[0m")
                raise NameError
            # Return whether the variable is set
            return self.variable_indexes[identifier]["set"]
        else:
            # Check for undeclared variable
            if identifier.identifier not in self.variable_indexes.keys():
                print(
                    f"\033[91mUse of undeclared variable '{identifier.identifier}'!\033[0m"
                )
                raise NameError
            # Check if array element is set
            if (
                identifier.idx != -1
                and not self.variable_indexes[identifier.identifier]["set"]
            ):
                return self.variable_indexes[identifier.identifier]["set"][
                    identifier.idx
                ]
            # Return whether the variable is set
            return self.variable_indexes[identifier.identifier]["set"]

    def get_info(self, identifier):
        """
        Retrieves all information about variable.
        :param identifier: id
        :return: dict
        """
        # Check for undeclared variable
        if identifier not in self.variable_indexes.keys():
            print(f"\033[91mUse of undeclared variable '{identifier}'!\033[0m")
            raise NameError
        # Return information about the variable
        return self.variable_indexes[identifier]

    def set_variable(self, identifier: ValInfo) -> None:
        """
        Sets a variable or array element as "set"
        :param identifier: id
        :return: None
        """
        if identifier.identifier is None:
            return
        if identifier.v_type == "AKU":
            if identifier.identifier[0] not in self.variable_indexes.keys():
                print(
                    f"\033[91mUse of undeclared variable '{identifier.identifier[0]}'!\033[0m"
                )
                raise NameError
            self.variable_indexes[identifier.identifier[0]]["set"] = True

        else:
            if identifier.identifier not in self.variable_indexes.keys():
                print(
                    f"\033[91mUse of undeclared variable '{identifier.identifier}'!\033[0m"
                )
                raise NameError
            elif (
                identifier.idx != -1
                and not self.variable_indexes[identifier.identifier]["set"]
            ):
                self.variable_indexes[identifier.identifier]["set"][
                    identifier.idx
                ] = True
            else:
                self.variable_indexes[identifier.identifier]["set"] = True
