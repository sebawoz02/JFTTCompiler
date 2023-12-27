def add_sub(cg, value1, value2, mode='add') -> (None, str, int):
    if value1[1] == 'NUM' and value2[1] == 'NUM':
        return value1[0] + value2[0], 'NUM', 0
    lines = 0
    if value2[1] == 'PIDENTIFIER':
        lines += cg.get_number_in_register(value2[0], 'h') + 2
        cg.write("LOAD h\n")
        cg.write("PUT c\n")
    elif value2[1] == 'AKU':
        lines += cg.load_aku_idx(value2[0][0], value2[0][1]) + 2
        cg.write("LOAD a\n")
        cg.write("PUT c\n")
    else:
        lines += cg.get_number_in_register(value2[0], 'c')
    if value1[1] == 'PIDENTIFIER':
        lines += cg.get_number_in_register(value1[0], 'h') + 1
        cg.write("LOAD h\n")
    elif value1[1] == 'AKU':
        lines += cg.load_aku_idx(value1[0][0], value1[0][1]) + 1
        cg.write("LOAD a\n")
    else:
        lines += cg.get_number_in_register(value1[0], 'a')
    if mode == 'add':
        cg.write("ADD c\n")
    else:
        cg.write("SUB c\n")
    return None, 'EXPRESSION', lines + 1


def multiply(cg, value1, value2) -> (None, str, int):
    if value1[1] == 'NUM' and value2[1] == 'NUM':
        return value1[0] * value2[0], 'NUM', 0
    lines = 0
    # Prepare registers
    if value2[1] == 'PIDENTIFIER':
        lines += cg.get_number_in_register(value2[0], 'h') + 1
        cg.write("LOAD h\n")
        cg.write("PUT c\n")
    elif value2[1] == 'AKU':
        lines += cg.load_aku_idx(value2[0][0], value2[0][1]) + 2
        cg.write("LOAD a\n")
        cg.write("PUT c\n")
    else:
        lines += cg.get_number_in_register(value2[0], 'c')
    if value1[1] == 'PIDENTIFIER':
        lines += cg.get_number_in_register(value1[0], 'h') + 2
        cg.write("LOAD h\n")
        cg.write("PUT b\n")
    elif value1[1] == 'AKU':
        lines += cg.load_aku_idx(value1[0][0], value1[0][1]) + 2
        cg.write("LOAD a\n")
        cg.write("PUT b\n")
    else:
        lines += cg.get_number_in_register(value1[0], 'b')
    # Multiplication algorithm
    cg.write("RST d\n")
    init_lines = cg.line
    cg.write("GET c\n")     #
    cg.write("SHR a\n")     # JODD - c is odd number
    cg.write("SHL a\n")     #
    cg.write("INC a\n")     #
    cg.write("SUB c\n")     #
    cg.write(f"JPOS {cg.line + 4}\n")   # if
    cg.write("GET d\n")
    cg.write("ADD b\n")
    cg.write("PUT d\n")
    cg.write("SHL b\n")     # jump
    cg.write("SHR c\n")
    cg.write("GET c\n")
    cg.write("DEC a\n")
    cg.write(f"JPOS {init_lines}\n")
    cg.write("GET d\n")
    cg.write("ADD b\n")
    return None, 'EXPRESSION', lines + 17

