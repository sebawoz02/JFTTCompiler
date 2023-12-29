def _exit(par, string):
    par.cg.close()
    print(string)
    print("Compilation failed!")
    exit(1)


def EXCEPTION_WRAPPER(par, ex, func, *args):
    try:
        return func(*args)
    except ex:
        par.cg.close()
        print("Compilation failed!")
        exit(1)


def check_if_set(par, pp, p, warnings, mode='error'):
    def error_msg():
        if mode == 'error':
            _exit(par, f"\033[91mUse of unset variable '{pp.identifier}' in line {p.lineno}!\033[0m")
        elif "unset" in warnings:
            print(f"WARNING! Use of unset variable in {mode}. line={p.lineno}.")

    if par.cg.block_level > 0:
        mode = "conditional scope"
    if par.pg.definition:
        if pp.v_type == "PIDENTIFIER":
            if not par.pg.is_set(pp):
                error_msg()
        elif pp.v_type == "AKU":
            if pp.identifier is None:
                return
            if not par.pg.is_set(pp.identifier[0]) and par.pg.is_set(pp.identifier[1]):
                error_msg()
    elif pp.v_type == "PIDENTIFIER":
        if not par.allocator.is_set(pp):
            if mode == 'error':
                _exit(par, f"\033[91mUse of unset variable '{pp.identifier}' in line {p.lineno}!\033[0m")
            elif "unset" in warnings:
                print(f"WARNING! Use of unset variable in {mode}. line={p.lineno}.")
    elif pp.v_type == "AKU":
        if not par.allocator.is_set(pp.identifier[0]) and par.allocator.is_set(pp.identifier[1]):
            error_msg()


def check_if_not_array(par, pp, p):
    if par.pg.definition:
        info = par.EXCEPTION_WRAPPER(NameError, par.pg.get_param_info, pp)
        if info['type'] == 'T':
            _exit(par, f"\033[91mProhibited use of array type variable '{pp}' in line {p.lineno}!\033[0m")
    else:
        info = par.EXCEPTION_WRAPPER(NameError, par.allocator.get_type, pp)
        if info == 'T':
            _exit(par, f"\033[91mProhibited use of array type variable '{pp}' in line {p.lineno}!\033[0m")


def check_if_array(par, pp, p):
    if par.pg.definition:
        info = par.EXCEPTION_WRAPPER(NameError, par.pg.get_param_info, pp)
        if info['type'] == '1':
            _exit(par, f"\033[91mProhibited use of int type variable '{pp}' in line {p.lineno}!\033[0m")
    else:
        info = par.EXCEPTION_WRAPPER(NameError, par.allocator.get_type, pp)
        if info == '1':
            _exit(par, f"\033[91mProhibited use of int type variable '{pp}' in line {p.lineno}!\033[0m")


def check_if_index_in_range(par, pp, num, p):
    if par.pg.definition:
        info = par.EXCEPTION_WRAPPER(NameError, par.pg.get_param_info, pp)
        if info['size'] <= num and info['size'] != -1:
            _exit(par, f"\033[91mArray '{pp}' index {num} out of range! Line {p.lineno}.\033[0m")
    else:
        info = par.EXCEPTION_WRAPPER(NameError, par.allocator.get_info, pp)
        if info['size'] <= num:
            _exit(par, f"\033[91mArray '{pp}' index {num} out of range! Line {p.lineno}.\033[0m")
