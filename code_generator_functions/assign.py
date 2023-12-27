# PIDENTIFIER ASSIGN NUM
# save the number at a given index in memory
# Returns number of lines written
def assign_number(cg, num, idx, address_in_c=False):
    # Get expected number in register a
    lines = cg.get_number_in_register(num, 'a')
    if address_in_c:
        cg.write("STORE c\n")
        return lines + 1
    # Save it in memory
    return lines + cg.store(idx)


# PIDENTIFIER ASSIGN pidentifier
# save/copy the number from one index in memory under the other
# Returns number of lines written
def assign_identifier(cg, idx1, idx2, address_in_c=False):
    lines = cg.get_number_in_register(idx2, 'h')
    cg.write("LOAD h\n")
    if address_in_c:
        cg.write("STORE c\n")
        return lines + 2
    return lines + 1 + cg.store(idx1)


def assign_aku(cg, idx1, idx2, idx3, address_in_c=False):
    lines = cg.load_aku_idx(idx2, idx3)
    if address_in_c:
        cg.write("STORE c\n")
        return lines + 1
    return cg.store(idx1) + lines


# STORE
# save value from register 'a' at given idx in memory
# Returns number of lines written
def store(cg, idx):
    lines = cg.get_number_in_register(idx, 'h')
    cg.write("STORE h\n")
    return lines + 1


# Loads memory address of PIDENTIFIER[PIDENTIFIER] to register 'a'
def load_aku_idx(cg, idx1, idx2):
    lines = cg.get_number_in_register(idx1, 'b')
    lines += cg.get_number_in_register(idx2, 'a')
    cg.write('LOAD a\n')
    cg.write('ADD b\n')
    return lines + 2


def generate_assign(cg, identifier, expression):
    # p[2] = [idx, 'NUM'/'PIDENTIFIER'/'EXPRESSION', lines_of_code] or [(idx1, idx2), 'AKU', lines_of_code]
    if identifier[1] == 'AKU':
        lines = 0
        if expression[1] == 'EXPRESSION':
            cg.write("PUT c\n")
            lines += 1
        lines += cg.load_aku_idx(identifier[0][0], identifier[0][1])
        if expression[1] == 'EXPRESSION':
            cg.write("PUT b\n")
            cg.write("GET c\n")
            cg.write("STORE b\n")
            return lines + 3 + expression[2]
        else:
            cg.write("PUT c\n")
            lines += 1
        if expression[1] == 'NUM':
            return cg.assign_number(expression[0], identifier[0], address_in_c=True) + lines
        elif expression[1] == 'PIDENTIFIER':
            return cg.assign_identifier(identifier[0], expression[0], address_in_c=True) + lines
        else:
            return cg.assign_aku(identifier[0], expression[0][0], expression[0][1], address_in_c=True) + lines
    else:
        if expression[1] == 'NUM':
            return cg.assign_number(expression[0], identifier[0])
        elif expression[1] == 'PIDENTIFIER':
            return cg.assign_identifier(identifier[0], expression[0])
        elif expression[1] == 'AKU':
            return cg.assign_aku(identifier[0], expression[0][0], expression[0][1])
        else:
            return cg.store(identifier[0]) + expression[2]
