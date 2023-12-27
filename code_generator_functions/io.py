def command_write(cg, value):
    # value = [idx/number, 'NUM'/'PIDENTIFIER'/'EXPRESSION', lines_of_code]
    lines = 0
    if value[1] == 'NUM':
        lines += cg.get_number_in_register(value[0], 'a')
    elif value[1] == 'PIDENTIFIER':
        lines += cg.get_number_in_register(value[0], 'h') + 1
        cg.write('LOAD h\n')
    elif value[1] == 'AKU':
        lines += cg.load_aku_idx(value[0][0], value[0][1]) + 1
        cg.write("LOAD a\n")
    # if value[1] == 'EXPRESSION' its already in register a
    cg.write('WRITE\n')
    return lines + 1


def command_read(cg, value):
    cg.write("READ\n")
    lines = 1
    if value[1] == 'AKU':
        cg.write("PUT c\n")
        lines += cg.get_number_in_register(value[0][1], 'h') + 2
        cg.write("LOAD h\n")
        lines += cg.get_number_in_register(value[0][0], 'a') + 4
        cg.write("ADD h\n")
        cg.write("PUT b\n")
        cg.write("GET c\n")
        cg.write("STORE b\n")
    else:
        lines += cg.get_number_in_register(value[0], 'h') + 1
        cg.write("STORE h\n")
    return lines
