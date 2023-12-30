from value import ValInfo


def command_write(cg, value: ValInfo):
    lines = 0
    if value.v_type == 'NUM':
        lines += cg.get_number_in_register(value.value, 'a')
    elif value.v_type == 'PIDENTIFIER':
        lines += cg.get_number_in_register(value.value, 'address') + 1
        cg.write(f'LOAD {cg.last_used_address_register}\n')
    elif value.v_type == 'AKU':
        lines += cg.load_aku_idx(value.value[0], value.value[1]) + 1
        cg.write("LOAD a\n")
    # if value[1] == 'EXPRESSION' its already in register a
    cg.write('WRITE\n')
    return lines + 1


def command_read(cg, value: ValInfo):
    cg.write("READ\n")
    lines = 1
    if value.v_type == 'AKU':
        cg.write("PUT c\n")
        lines += cg.get_number_in_register(value.value[1], 'address') + 2
        cg.write(f"LOAD {cg.last_used_address_register}\n")
        lines += cg.get_number_in_register(value.value[0], 'a') + 4
        cg.write("ADD h\n")
        cg.write("PUT b\n")
        cg.write("GET c\n")
        cg.write("STORE b\n")
    else:
        lines += cg.get_number_in_register(value.value, 'address') + 1
        cg.write(f"STORE {cg.last_used_address_register}\n")
    return lines
