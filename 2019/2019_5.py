class Instruction:
    def __init__(self, instruction, memory, opcodes, address, input_var=1):
        self.instruction = instruction
        self.opcodes = opcodes
        self.memory = memory
        self.address = address
        self.input_var = input_var

    def parse_instruction(self):
        self.opcode, param_length = self.opcodes[int(str(self.instruction)[-2:])]
        if self.instruction > 99:
            read_modes = [int(i) for i in str(self.instruction)[:-2]]
            read_modes.reverse()
        else:
            read_modes = [] 
        while len(read_modes) < param_length:
            read_modes.append(0)

        self.params = []
        for i in range(param_length):
            self.params.append(Param(self.memory, self.address+1+i, read_modes[i]))
        
        return self.opcode, self.params

    def execute(self, pointer):
        self.output_var, pointer = self.opcode(self.params, self.input_var, pointer)
        return self.output_var, pointer


class Param:
    def __init__(self, memory, address, read_mode):
        self.memory = memory
        self.address = address
        self.read_mode = read_mode

        self.readers = {
            0: self.position_mode,
            1: self.immediate_mode,
        }

        if address >= len(memory) or address <0:
           raise Exception(f'address out of memory. Address is {address}, memory length is {len(memory)}') 

    def write(self, val):
        self.memory[self.memory[self.address]] = val

    def read(self):
        return self.readers[self.read_mode]()

    def position_mode(self):
        return self.memory[self.memory[self.address]]

    def immediate_mode(self):
        return self.memory[self.address]


class Program:
    def __init__(self, memory, opcodes, noun, verb, input_var=1):
        self.memory = list(memory)
        self.memory[1] = self.memory[1] if noun is None else noun
        self.memory[2] = self.memory[2] if verb is None else verb
        self.pointer = 0
        self.opcodes = opcodes
        self.input_var = input_var

    def run_one_step(self, input_var=None):
        input_var = input_var or self.input_var
        if not isinstance(self.pointer, int):
            return f"Program halted: {self.pointer}"

        instruction = Instruction(self.memory[self.pointer], self.memory, self.opcodes, self.pointer, input_var)
        instruction.parse_instruction()
        output_var, self.pointer = instruction.execute(self.pointer)
        return output_var
    
    def run(self, input_var=None):
        input_var = input_var or self.input_var
        while True:
            instruction = Instruction(self.memory[self.pointer], self.memory, self.opcodes, self.pointer, input_var)
            instruction.parse_instruction()
            output_var, self.pointer = instruction.execute(self.pointer)
            if output_var is not None:
                print(output_var)
            if output_var == 'halt':
                return 'Program halted'

# Opcodes
def opcode_1(params, input_var, pointer):
    params[2].write(params[0].read() + params[1].read())
    return None, pointer+4

def opcode_2(params, input_var, pointer):
    params[2].write(params[0].read() * params[1].read())
    return None, pointer+4

def opcode_3(params, input_var, pointer):
    params[0].write(input_var)
    return None, pointer+2

def opcode_4(params, input_var, pointer):
    return params[0].read(), pointer+2

def opcode_5(params, input_var, pointer):
    if params[0].read() == 0:
        return None, pointer+3
    else:
        return None, params[1].read()

def opcode_6(params, input_var, pointer):
    if params[0].read() == 0:
        return None, params[1].read()
    else:
        return None, pointer+3

def opcode_7(params, input_var, pointer):
    if params[0].read() < params[1].read():
        params[2].write(1)
    else:
        params[2].write(0)
    return None, pointer+4

def opcode_8(params, input_var, pointer):
    if params[0].read() == params[1].read():
        params[2].write(1)
    else:
        params[2].write(0)
    return None, pointer+4

def opcode_99(params, input_var, pointer):
    return 'halt', pointer+1

opcodes = {
    99: (opcode_99, 0),
    1: (opcode_1, 3),
    2: (opcode_2, 3),
    3: (opcode_3, 1),
    4: (opcode_4, 1),
    5: (opcode_5, 2),
    6: (opcode_6, 2),
    7: (opcode_7, 3),
    8: (opcode_8, 3),
}

# Test cases:
test1 = [1,0,0,0,99] # 2,0,0,0,99
test2 = [2,3,0,3,99] # 2,3,0,6,99
test3 = [2,4,4,5,99,0] # 2,4,4,5,99,9801
test4 = [1,1,1,4,99,5,6,0,99] # 30,1,1,4,2,5,6,0,99

test1_program = Program(test1, opcodes, None, None)
test1_program.run()
test2_program = Program(test2, opcodes, None, None)
test2_program.run()
test3_program = Program(test3, opcodes, None, None)
test3_program.run()
test4_program = Program(test4, opcodes, None, None)
test4_program.run()


input_file_test = open("./2019/2019_2_input.txt", 'r').read()
input_file_test = [int(i) for i in input_file_test.strip().split(',')]
print(input_file_test)
test_input_program = Program(input_file_test, opcodes, 12, 2)
test_input_program.run()

print(test1_program.memory)
print(test2_program.memory)
print(test3_program.memory)
print(test4_program.memory)
print(test_input_program.memory[0])


input_file = open("./2019/2019_5_input.txt", 'r').read()
input_file = [int(i) for i in input_file.strip().split(',')]
input_program = Program(input_file, opcodes, None, None)
input_program.run()


test_5 = [3,9,8,9,10,9,4,9,99,-1,8] # Outputs 1 if input is 8, 0 otherwise
test_6 = [3,9,7,9,10,9,4,9,99,-1,8] # Outputs 1 is input < 8, 0 otherwise
test_7 = [3,3,1108,-1,8,3,4,3,99] # Outputs 1 if input is 8, 0 otherwise
test_8 = [3,3,1107,-1,8,3,4,3,99] # Outputs 1 if input < 8, 0 otherwise
test_9 = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9] # Output 1 is input != 0, 0 otherwise
test_10 = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1] # Output 1 is input != 0, 0 otherwise
test_11 = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
           1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
           999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99] # Output 999 is input < 8, 1000 if == 8, 1001 if greater

test_11_5 = Program(test_11, opcodes, None, None, 5)
test_11_5.run()
test_11_8 = Program(test_11, opcodes, None, None, 8)
test_11_8.run()
test_11_99 = Program(test_11, opcodes, None, None, 99)
test_11_99.run()


part2_input_program = Program(input_file, opcodes, None, None, 5)
part2_input_program.run()
    