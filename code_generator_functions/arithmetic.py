from value import ValInfo


def _prep_registers(cg, value1: ValInfo, value2: ValInfo):
    lines = 0
    if value2.v_type == 'PIDENTIFIER':
        lines += cg.get_number_in_register(value2.value, 'h') + 1
        cg.write("LOAD h\n")
        cg.write("PUT c\n")
    elif value2.v_type == 'AKU':
        lines += cg.load_aku_idx(value2.value[0], value2.value[1]) + 2
        cg.write("LOAD a\n")
        cg.write("PUT c\n")
    else:
        lines += cg.get_number_in_register(value2.value, 'c')
    if value1.v_type == 'PIDENTIFIER':
        lines += cg.get_number_in_register(value1.value, 'h') + 2
        cg.write("LOAD h\n")
        cg.write("PUT b\n")
    elif value1.v_type == 'AKU':
        lines += cg.load_aku_idx(value1.value[0], value1.value[1]) + 2
        cg.write("LOAD a\n")
        cg.write("PUT b\n")
    else:
        lines += cg.get_number_in_register(value1.value, 'b')
    return lines


# + and  -
def add_sub(cg, value1: ValInfo, value2: ValInfo, mode='add') -> ValInfo:
    if value1.v_type == 'NUM' and value2.v_type == 'NUM':
        if mode == 'add':
            return ValInfo(value1.value + value2.value, 'NUM', 0)
        else:
            return ValInfo(max(value1.value - value2.value, 0), 'NUM', 0)
    lines = 0
    if value2.v_type == 'PIDENTIFIER':
        lines += cg.get_number_in_register(value2.value, 'h') + 2
        cg.write("LOAD h\n")
        cg.write("PUT c\n")
    elif value2.v_type == 'AKU':
        lines += cg.load_aku_idx(value2.value[0], value2.value[1]) + 2
        cg.write("LOAD a\n")
        cg.write("PUT c\n")
    else:
        lines += cg.get_number_in_register(value2.value, 'c')
    if value1.v_type == 'PIDENTIFIER':
        lines += cg.get_number_in_register(value1.value, 'h') + 1
        cg.write("LOAD h\n")
    elif value1.v_type == 'AKU':
        lines += cg.load_aku_idx(value1.value[0], value1.value[1]) + 1
        cg.write("LOAD a\n")
    else:
        lines += cg.get_number_in_register(value1.value, 'a')
    if mode == 'add':
        cg.write("ADD c\n")
    else:
        cg.write("SUB c\n")
    return ValInfo(None, 'EXPRESSION', lines + 1)


# *
def multiply(cg, value1: ValInfo, value2: ValInfo) -> ValInfo:
    if value1.v_type == 'NUM' and value2.v_type == 'NUM':
        return ValInfo(value1.value * value2.value, 'NUM', 0)
    # Prepare registers
    lines = _prep_registers(cg, value1, value2)
    cg.write("RST d\n")

    # Multiplication algorithm
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
    return ValInfo(None, 'EXPRESSION', lines + 17)


# / and %
def divide(cg, value1: ValInfo, value2: ValInfo, mode) -> ValInfo:
    if value1.v_type == 'NUM' and value2.v_type == 'NUM':
        if value2.value == 0:
            return ValInfo(0, 'NUM', 0)
        if mode == 'div':
            return ValInfo(value1.value / value2.value, 'NUM', 0)
        else:
            return ValInfo(value1.value % value2.value, 'NUM', 0)
    # Prepare registers
    lines = _prep_registers(cg, value1, value2) + 1
    if mode == 'div':
        cg.write("RST e\n")
        lines += 1
    cg.write("RST d\n")

    # Division algorithm    - b - dividend, c - divisor, d - remainder, e - quotient, f - buffer
    init_line = cg.line
    cg.write("SHL d\n")

    cg.write("GET b\n")  #
    cg.write("SHR a\n")  # JODD - dividend is odd number
    cg.write("SHL a\n")  #
    cg.write("INC a\n")  # THIS IS WRONG
    cg.write("SUB b\n")  #
    cg.write(f"JPOS {cg.line + 8}\n")
    cg.write("GET d\n")  #
    cg.write("SHR a\n")  # JEVEN - remainder is even number
    cg.write("SHL a\n")  #
    cg.write("INC a\n")  #
    cg.write("SUB d\n")  #
    cg.write(f"JZERO {cg.line + 2}\n")
    cg.write("INC d\n")  # remainder |= dividend & 1

    cg.write("SHR b\n")  # dividend >> 1

    cg.write("GET c\n")
    cg.write("SUB d\n")
    if mode == 'div':
        cg.write(f"JPOS {cg.line + 13}\n")
    else:
        cg.write(f"JPOS {cg.line + 4}\n")  # if divisor <= remainder
    cg.write("GET d\n")
    cg.write("SUB c\n")
    cg.write("PUT d\n")
    if mode == 'div':
        cg.write("RST f\n")
        cg.write("GET b\n")
        cg.write(f"JZERO {cg.line + 4}\n")
        cg.write("INC f\n")
        cg.write("SHR a\n")
        cg.write(f"JUMP {cg.line - 3}\n")
        cg.write("GET e\n")
        cg.write("ADD f\n")
        cg.write("PUT e\n")
        lines += 9

    cg.write("GET b\n")
    cg.write(f"JPOS {init_line}\n")
    if mode == 'modulo':
        cg.write("GET d\n")
    else:
        cg.write("GET e\n")

    return ValInfo(None, 'EXPRESSION', lines + 25)
