import re


def flush_block_buffer(cg, line_num):
    # JPOS/JZERO line_num
    cg.block_level -= 1
    cg.block_buffer[cg.block_level][0] += f'{line_num}\n'
    if cg.block_level == 0:
        for line in cg.block_buffer[0]:
            cg.code_file.write(line)
    else:
        # Merge nested block
        for line in cg.block_buffer[cg.block_level]:
            cg.block_buffer[cg.block_level - 1].append(line)
    cg.block_buffer.pop()


def fix_else_jumps(cg, idx):
    for i in range(idx, len(cg.block_buffer[cg.block_level - 1])):
        # Check if the string begins with 'JUMP', 'JPOS', or 'JZERO'
        if cg.block_buffer[cg.block_level - 1][i].startswith(('JUMP', 'JPOS', 'JZERO')):
            match = re.search(r'\d+', cg.block_buffer[cg.block_level - 1][i])
            if match:
                # Increase the number by 1
                number = int(match.group()) + 1
                cg.block_buffer[cg.block_level - 1][i] = re.sub(r'\d+',
                                                                str(number),
                                                                cg.block_buffer[cg.block_level - 1][i])
