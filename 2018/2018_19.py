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


opcodes = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]


def part_1():
    input_file = open('2018_16_input.txt', 'r').read().splitlines()
    commands = []
    for i in range(0, 3044, 4):
        before = eval(input_file[i][8:20])
        instruction = [int(j) for j in input_file[i+1].split()]
        after = eval(input_file[i+2][8:20])
        commands.append([before, instruction, after])
    print(commands)
    commands_with_3 = []
    for command in commands:
        opcode_match = 0
        for opcode in opcodes:
            opcode_result = opcode(command[0], *command[1][1:])
            if opcode_result == command[2]:
                opcode_match += 1
        if opcode_match >= 3:
            commands_with_3.append(command)
    print(len(commands_with_3))


def part_2():
    input_file = open('2018_16_input.txt', 'r').read().splitlines()
    commands = []
    for i in range(0, 3044, 4):
        before = eval(input_file[i][8:20])
        instruction = [int(j) for j in input_file[i+1].split()]
        after = eval(input_file[i+2][8:20])
        commands.append([before, instruction, after])
    print(commands)
    opcode_poss = {i: [opcode for opcode in opcodes] for i in range(len(opcodes))}
    for command in commands:
        to_remove = []
        for opcode in opcode_poss[command[1][0]]:
            opcode_result = opcode(command[0], *command[1][1:])
            if opcode_result != command[2]:
                opcode_poss[command[1][0]].remove(opcode)
    print(opcode_poss)
    for i in range(9):
        for i in opcode_poss:
            if len(opcode_poss[i]) == 1:
                for j in opcode_poss:
                    if i != j and opcode_poss[i][0] in opcode_poss[j]:
                        opcode_poss[j].remove(opcode_poss[i][0])
    print(opcode_poss)

    input_commands = [[int(j) for j in i.split()] for i in input_file[3046:]]
    print(input_commands)
    registers = [0, 0, 0, 0]
    for i in input_commands:
        registers = opcode_poss[i[0]][0](registers, *i[1:])
    print(registers)


part_1()
part_2()
solved_opcodes = [eqir, seti, eqri, eqrr, addi, setr, gtrr, gtri, muli, bori, bani, borr, gtir, banr, addr, mulr]
opcodes_call = {'eqir': eqir,
                'seti':  seti,
                'eqri': eqri,
                'eqrr': eqrr,
                'addi': addi,
                'setr': setr,
                'gtrr': gtrr,
                'gtri': gtri,
                'muli': muli,
                'bori': bori,
                'bani': bani,
                'borr': borr,
                'gtir': gtir,
                'banr': banr,
                'addr': addr,
                'mulr': mulr}


def run_function(registers, a, b, c, function):
    registers = registers[:]
    registers = function(registers, a, b, c)
    return registers


input_file = open('2018_19_input.txt', 'r').read().splitlines()
commands = [line.split() for line in input_file[1:]]
for i in range(len(commands)):
    print(i, commands[i])
input_file_test = open('2018_19_test.txt', 'r').read().splitlines()
test_commands = [line.split() for line in input_file_test[1:]]
print(test_commands)


def part_1_19(ip_r, inputs, registers):
    registers = registers[:]
    while 0 <= registers[ip_r] < len(inputs):
        print(registers)
        ip = registers[ip_r]
        registers = run_function(registers, int(inputs[ip][1]), int(inputs[ip][2]), int(inputs[ip][3]),
                                 opcodes_call[inputs[ip][0]])
        print(registers)
        registers[ip_r] += 1


def part_2_19():
    registers = [1, 0, 0, 0, 0, 0]
    functions = {0: func_0, 1: func_1, 2: func_2, 3: func_3, 8: func_1, 17: func_17}
    return func_0(registers, functions)


def func_0(registers, functions):
    registers = registers[:]
    # function 17 is only run once, this time, so:
    # return functions[17](registers, functions)
    # registers[4] = 160  # (7 * 22) + 6
    # registers[3] = 996  # 836 (2*2*19*11) + 160
    # registers[0] starts with value 1 in part 2
    # if registers[0] == 0:
    #     return functions[1](registers, functions)
    # else:
    # registers[2] += registers[0]
    # return functions[registers[2]](registers, functions)
    registers[4] = 390516  # 27 * 28 + 29 * 30 * 14 * 32
    registers[3] = 391512  # 27 * 28 + 29 * 30 * 14 * 32 + 996
    registers[0] = 0
    return func_1_first_time(registers, functions)


def func_1_first_time(registers, functions):
    registers = registers[:]
    registers[1] = 1
    registers[5] = 1
    registers[4] = 0
    registers[0] = 1
    return func_8_first_time(registers, functions)


def func_1(registers, functions):
    registers = registers[:]
    registers[1] = 1
    registers[5] = 1
    if registers[3] == 1:
        registers[4] = 1
        return functions[8](registers, functions)
    else:
        registers[4] = 0
        registers[0] += 1
        return functions[8](registers, functions)


def func_2(registers, functions):
    registers = registers[:]
    registers[5] = 1
    if registers[3] == registers[1]:
        registers[4] = 1
        return functions[8](registers, functions)
    else:
        registers[4] = 0
        registers[0] += 1
        return functions[8](registers, functions)


def func_3_first_time(registers, functions):
    registers[5] = 2
    registers[1] = 1
    registers[4] = 0
    registers[0] = 1
    registers[3] = 391512  # 27 * 28 + 29 * 30 * 14 * 32 + 996
    registers[0] += 1


def func_3(registers, functions):
    if registers[3] == registers[1]*registers[5]:
        registers[4] = 1
        return functions[8](registers, functions)
    else:
        registers[4] = 0
        registers[0] += 1
        return functions[8](registers, functions)


def func_8_first_time(registers, functions):
    registers = registers[:]
    registers[5] = 2
    return func_3_first_time(registers, functions)


def func_8(registers, functions):
    registers = registers[:]
    registers[5] += 1
    if registers[5] <= registers[3]:
        registers[4] = 0
        return functions[3](registers, functions)
    else:
        registers[1] += 1
        if registers[1] <= registers[3]:
            registers[4] = 0
            return functions[2](registers, functions)
        else:
            registers[4] = 1
            return registers


def func_17(registers, functions):
    registers = registers[:]
    registers[3] = 11 * registers[2]*((registers[3]+2)**2)
    registers[4] = ((registers[4] + 7) * 2) + 6
    registers[3] = registers[3]+registers[4]
    if registers[0] == 0:
        return functions[1](registers, functions)
    else:
        registers[2] += registers[0]
        return functions[registers[2]](registers, functions)



import sys
sys.setrecursionlimit(1000000000)
print(len(commands))
part_1_19(0, test_commands, [0, 0, 0, 0, 0, 0])
# part_1_19(2, commands, [0, 0, 0, 0, 0, 0])
# part_1_19(2, commands, [1, 0, 0, 0, 0, 0])
print()
# print(part_2_19())

registers = [1, 1, 8, ]

def function_2():
    i = 8
    registers = [2, 1, 0, 391512, 0, 2]
    while i in (2, 3, 8):
        if i == 8:
            registers[5] += 1
            if registers[5] > registers[3]:
                registers[1] += 1
                if registers[1] > registers[3]:
                    i = 10
                    print(registers)
                else:
                    i = 2
            else:
                i = 3
        elif i == 2:
            registers[5] = 1
            if registers[3] == registers[1]:
                i = 8
            else:
                registers[0] += 1
                i = 8
        elif i == 3:
            if registers[3] == registers[1]*registers[5]:
                i = 8
            else:
                registers[0] += 1
                i = 8
        print(registers)


# function_2()

def function_3():
    i = 8
    registers = [1, 0, 0, 0, 0, 0]
    i = 17
    registers[3] += 2
    registers[3] *= registers[3]
    registers[3] = registers[3] * 19
    registers[3] = registers[3] * 11
    registers[4] = 7
    registers[4] = registers[4] * 22
    registers[4] += 6
    registers[3] += registers[4]
    registers[4] = 27
    registers[4] = registers[4] * 28
    registers[4] = registers[4] + 29
    registers[4] = registers[4] * 30
    registers[4] = registers[4] * 14
    registers[4] = registers[4] * 32
    registers[3] = registers[3] + registers[4]
    registers[0] = 0
    i = 1
    registers[1] = 1
    i = 2
    # registers[3] = 10
    while i in (2, 3, 8):
        if i == 2:
            registers[5] = 1
            if registers[1] == registers[3]:
                registers[0] += registers[1]
                i = 8
            else:
                i = 8
        elif i == 3:
            if registers[3] == registers[1]*registers[5]:
                registers[0] += registers[1]
                i = 8
            else:
                i = 8
        elif i == 8:
            registers[5] += 1
            if registers[5] > registers[3]:
                registers[1] += 1
                if registers[1] > registers[3]:
                    i = 10
                    print(registers)
                else:
                    i = 2
            else:
                i = 3
        print(registers)


# function_3()


def find_factors(number):
    factors = []
    mult = 1
    relevant_factor = number
    for i in range(1, number+1):
        if i >= relevant_factor:
            print(factors)
            break
        if number % i == 0:
            factors.append(i)
            factors.append(number/i)
            relevant_factor = number / i
    print(sum(factors))


find_factors(10551396)



