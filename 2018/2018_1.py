# Part 1
input_file = open('2018_1_input.txt', 'r')
frequency = 0
for line in input_file:
    if line[0] == '+':
        frequency = frequency + int(line[1:(len(line)-1)])
    else:
        frequency = frequency - int(line[1:(len(line)-1)])
print(frequency)

# Part 2
input_file = open('2018_1_input.txt', 'r').readlines()
frequency = 0
frequencies = set([0, ])
add_freq = frequencies.add
found = None
loop_num = 0
while found is None:
    loop_num += 1
    for line in input_file:
        if line[0] == '+':
            frequency += int(line[1:(len(line)-1)])
        else:
            frequency -= int(line[1:(len(line)-1)])
        if frequency in frequencies:
            found = frequency
            print(found, "in loop", loop_num)
            break
        else:
            add_freq(frequency)

