def addr(registers, a, b, c):
    registers = registers[:]
    registers[c] = registers[a] + registers[b]
    return registers


def addi(registers, a, b, c):
    registers = registers[:]
    registers[c] = registers[a] + b
    return registers


def mulr(registers, a, b, c):
    registers = registers[:]
    registers[c] = registers[a] * registers[b]
    return registers


def muli(registers, a, b, c):
    registers = registers[:]
    registers[c] = registers[a] * b
    return registers


def banr(registers, a, b, c):
    registers = registers[:]
    registers[c] = int(registers[a]) & int(registers[b])
    return registers


def bani(registers, a, b, c):
    registers = registers[:]
    registers[c] = int(registers[a]) & int(b)
    return registers


def borr(registers, a, b, c):
    registers = registers[:]
    registers[c] = int(registers[a]) | int(registers[b])
    return registers


def bori(registers, a, b, c):
    registers = registers[:]
    registers[c] = int(registers[a]) | int(b)
    return registers


def setr(registers, a, b, c):
    registers = registers[:]
    registers[c] = registers[a]
    return registers


def seti(registers, a, b, c):
    registers = registers[:]
    registers[c] = a
    return registers


def gtir(registers, a, b, c):
    registers = registers[:]
    registers[c] = 1 if a > registers[b] else 0
    return registers


def gtri(registers, a, b, c):
    registers = registers[:]
    registers[c] = 1 if registers[a] > b else 0
    return registers


def gtrr(registers, a, b, c):
    registers = registers[:]
    registers[c] = 1 if registers[a] > registers[b] else 0
    return registers


def eqir(registers, a, b, c):
    registers = registers[:]
    registers[c] = 1 if a == registers[b] else 0
    return registers


def eqri(registers, a, b, c):
    registers = registers[:]
    registers[c] = 1 if registers[a] == b else 0
    return registers


def eqrr(registers, a, b, c):
    registers = registers[:]
    registers[c] = 1 if registers[a] == registers[b] else 0
    return registers


opcodes = {'addr': addr,
           'addi': addi,
           'mulr': mulr,
           'muli': muli,
           'banr': banr,
           'bani': bani,
           'borr': borr,
           'bori': bori,
           'setr': setr,
           'seti': seti,
           'gtir': gtir,
           'gtri': gtri,
           'gtrr': gtrr,
           'eqir': eqir,
           'eqri': eqri,
           'eqrr': eqrr}


def run_func(func, registers, a, b, c):
    return opcodes[func](registers, a, b, c)


def run_instruction(instruction, registers):
    return opcodes[instruction[0]](registers, instruction[1], instruction[2], instruction[3])


def run_instructions(instructions, registers, ip):
    while 0 <= ip < len(instructions):
        registers = run_instruction(instructions[registers[ip]], registers)
        print(registers)
        registers[ip] += 1


def get_instructions(file):
    input_file = open(file, 'r').read().splitlines()
    ip = int(input_file[0].split()[1])
    lines_split = [line.split() for line in input_file[1:]]
    instructions = [[line[0], int(line[1]), int(line[2]), int(line[3])] for line in lines_split]
    return instructions, ip


def func_0(registers):
    print('0:', registers)
    registers = registers[:]
    if (123 & 456) != 72:
        return 'Infinite Loop'
    else:
        registers[4] = 0
        return func_6(registers)


def func_6(registers):
    print('6:', registers)
    registers = registers[:]
    registers[2] = 65536 | registers[4]
    registers[4] = 6152285
    return func_8(registers)


def func_8_old(registers):
    print('8:', registers)
    registers = registers[:]
    registers[4] = (((registers[4] + (registers[2] & 255)) & 16777215) * 65899) & 16777215
    if 256 > registers[2]:
        return func_28(registers)
    else:
        registers[1] = 0
        return func_18(registers)


def func_18_old(registers):
    print('18:', registers)
    registers = registers[:]
    registers[5] = (registers[1] + 1) * 256
    if registers[5] > registers[2]:
        registers[2] = registers[1]
        return func_8(registers)
    else:
        registers[1] = int((registers[2]/256) - 1) + 1
        return func_18_old(registers)


def func_8(registers):
    print(registers)
    registers = registers[:]
    registers[4] = (((registers[4] + (registers[2] & 255)) & 16777215) * 65899) & 16777215
    if 256 > registers[2]:
        if registers[4] == registers[0]:
            return registers
        else:
            registers[2] = 65536 | registers[4]
            registers[4] = 6152285
            return func_8(registers)
    else:
        registers[1] = int((registers[2] / 256) - 1) + 1
        registers[5] = (registers[1] + 1) * 256
        registers[2] = registers[1]
        return func_8(registers)


def function(registers):
    registers = registers[:]
    registers[2] = 65536
    registers[4] = 6152285
    while True:
        print(registers)
        registers[4] = (((registers[4] + (registers[2] & 255)) & 16777215) * 65899) & 16777215
        if 256 > registers[2]:
            if registers[4] == registers[0]:
                return registers
            else:
                registers[2] = 65536 | registers[4]
                registers[4] = 6152285
        else:
            registers[2] = int((registers[2] / 256) - 1) + 1


def function_2(registers):
    registers = registers[:]
    possible_4s = []
    registers[2] = 65536
    registers[4] = (((6152285 + (registers[2] & 255)) & 16777215) * 65899) & 16777215
    while True:
        if 256 > registers[2]:
            if registers[4] not in possible_4s:
                possible_4s.append(registers[4])
            print('List Length:', len(possible_4s))
            print(possible_4s[-1])
            if registers[4] == registers[0]:
                return registers
            else:
                registers[2] = 65536 | registers[4]
                registers[4] = (((6152285 + (registers[2] & 255)) & 16777215) * 65899) & 16777215
        else:
            registers[2] = int(registers[2] / 256) # Shift bits 8 to the left
            registers[4] = (((registers[4] + (registers[2] & 255)) & 16777215) * 65899) & 16777215


def function_3(registers):
    registers = registers[:]
    possible_4s = []
    registers[4] = 0
    registers[2] = 65536 | 0
    registers[4] = 6152285
    while True:
        registers[4] = ((((registers[2] & 255) + registers[4]) & 16777215) * 65899) & 16777215
        if 256 > registers[2]:
            if registers[4] not in possible_4s:
                possible_4s.append(registers[4])
                print(possible_4s[-1])
            if registers[4] == registers[0]:
                return registers
            else:
                registers[2] = 65536 | registers[4]
                registers[4] = 6152285
        else:
            registers[2] = int(registers[2] / 256)


def func_18(registers):
    print('18:', registers)
    registers = registers[:]
    registers[1] = int((registers[2] / 256) - 1) + 1
    registers[5] = (registers[1] + 1) * 256
    registers[2] = registers[1]
    # func 8:
    return func_8(registers)


def func_28(registers):
    print('28:', registers)
    registers = registers[:]
    # print(registers[4])
    if registers[4] == registers[0]:
        return registers
    else:
        return func_6(registers)


print(405429429215 & 16777215)
registers = [0, 0, 0, 0, 0, 0]
instructions, ip = get_instructions('2018_21_input.txt')
print(len(instructions))
function_3(registers)
