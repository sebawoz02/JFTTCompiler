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
