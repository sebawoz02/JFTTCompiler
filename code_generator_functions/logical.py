def op_eq(cg, value1, value2):
    # EQ - max(v1 - v2, 0) + max(v2 - v1, 0) == 0
    lines = cg.add_sub(value1, value2, mode='sub').lines
    cg.write('PUT d\n')
    lines += cg.add_sub(value2, value1, mode='sub').lines
    cg.write('ADD d\n')
    cg.inc_block_level()
    cg.write('JPOS ')
    return lines + 3


def op_neq(cg, value1, value2):
    # NEQ - max(v1 - v2, 0) + max(v2 - v1, 0) > 0
    lines = cg.add_sub(value1, value2, mode='sub').lines
    cg.write('PUT d\n')
    lines += cg.add_sub(value2, value1, mode='sub').lines
    cg.write('ADD d\n')
    cg.inc_block_level()
    cg.write('JZERO ')
    return lines + 3


def op_gt(cg, value1, value2):
    # GT - max(v1 - v2, 0) > 0
    lines = cg.add_sub(value1, value2, mode='sub').lines
    cg.inc_block_level()
    cg.write('JZERO ')
    return lines + 1


def op_lt(cg, value1, value2):
    # LT - max(v2 - v1, 0) > 0
    lines = cg.add_sub(value2, value1, mode='sub').lines
    cg.inc_block_level()
    cg.write('JZERO ')
    return lines + 1


def op_geq(cg, value1, value2):
    # GEQ - max(v2 - v1, 0) == 0
    lines = cg.add_sub(value2, value1, mode='sub').lines
    cg.inc_block_level()
    cg.write('JPOS ')
    return lines + 1


def op_leq(cg, value1, value2):
    # LEQ - max(v1 - v2, 0) == 0
    lines = cg.add_sub(value1, value2, mode='sub').lines
    cg.inc_block_level()
    cg.write('JPOS ')
    return lines + 1
