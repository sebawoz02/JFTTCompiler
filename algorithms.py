# Calculates the quickest way from 1 to x using only SHL, INC or DEC
def reach_target_number(x):
    operations = []

    while x != 1:
        if x % 2 == 0:
            x //= 2
            operations.append("SHL")
        elif (x - 1) % 4 == 0 or x == 3:
            x -= 1
            operations.append("INC")
        else:
            x += 1
            operations.append("DEC")

    return operations[::-1]
