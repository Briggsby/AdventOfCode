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
