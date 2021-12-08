input_file = open("./2019/2019_2_input.txt", 'r').read()
input_file = [int(i) for i in input_file.strip().split(',')]

def opcode_1(memory, pointer):
    memory[memory[pointer+3]] = memory[memory[pointer+1]] + memory[memory[pointer+2]]
    return memory, pointer+4

def opcode_2(memory, pointer):
    memory[memory[pointer+3]] = memory[memory[pointer+1]] * memory[memory[pointer+2]]
    return memory, pointer+4

def halt(memory, pointer):
    return memory, f"halt at {pointer}"

def compute(memory, pointer, opcodes):
    memory, pointer = opcodes[memory[pointer]](memory, pointer)
        
    if isinstance(pointer, int):
        if pointer > 0 & pointer < len(memory):
            return compute(memory, pointer, opcodes)
        elif pointer > len(memory):
            return memory, "ERR: Pointer outside memory"
        elif pointer < 0:
            return memory, "ERR: Pointer less than 0"
    else:
        return memory, pointer


def run(memory, noun, verb, opcodes):
    memory = list(memory)
    memory[1] = memory[1] if noun is None else noun
    memory[2] = memory[2] if verb is None else verb
    memory, result = compute(memory, 0, opcodes)
    return memory[0], result, memory


opcodes = {1: opcode_1, 2:opcode_2, 99: halt}

# Test cases:
test1 = [1,0,0,0,99]
test2 = [2,3,0,3,99]
test3 = [2,4,4,5,99,0]
test4 = [1,1,1,4,99,5,6,0,99]

print(run(test1, None, None, opcodes))
print(run(test2, None, None, opcodes))
print(run(test3, None, None, opcodes))
print(run(test4, None, None, opcodes))
print(run(input_file, 12, 2, opcodes))

for noun in range(100):
    for verb in range(100):
        if run(input_file, noun, verb, opcodes)[0] == 19690720:
            print(100 * noun + verb)


