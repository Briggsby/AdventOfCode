import time

# Part 1
input_file = open('2018_2_input.txt', 'r').read().splitlines()
double_lines = 0
triple_lines = 0
for line in input_file:
    singles = []
    doubles = []
    triples = []
    mores = []

    single = singles.append
    non_single = singles.remove
    double = doubles.append
    non_double = doubles.remove
    triple = triples.append
    non_triple = triples.remove
    more = mores.append

    for letter in line:
        if letter in singles:
            non_single(letter)
            double(letter)
        elif letter in doubles:
            non_double(letter)
            triple(letter)
        elif letter in triples:
            non_triple(letter)
            more(letter)
        elif letter not in mores:
            single(letter)
    if len(doubles) > 0:
        double_lines += 1
    if len(triples) > 0:
        triple_lines += 1
print(double_lines*triple_lines)

# Part 2 Method 1
# I thought this way would be faster than the obvious solution below it
# but was actually much slower
# For larger inputs a more optimized version of this might be faster though

start = time.time()

input_file = open('2018_2_input.txt', 'r').read().splitlines()
indices = {'a1': []}
common_1 = None
common_2 = None
line_index = 0
while common_1 is None and line_index < len(input_file):
    line = input_file[line_index]
    line_length = len(line)
    # Get all indexes of lines with letters in same places
    line_indices = []
    uniques = []
    for i in range(len(line)):
        letter = line[i]
        letter_pos = letter+str(i)
        if letter_pos in indices:
            for index in indices[letter_pos]:
                line_indices.append(index)
                if index not in uniques:
                    uniques.append(index)
    # Check for any with length-1 common letters
    for index in uniques:
        if line_indices.count(index) == line_length-1:
            common_1 = input_file[index]
            common_2 = line
            break
    # If none, add this line's letters to the list
    for i in range(len(line)):
        letter = line[i]
        letter_pos = line[i]+str(i)
        if letter_pos in indices:
            indices[letter_pos].append(line_index)
        else:
            indices[letter_pos] = [line_index]
    line_index += 1

if common_1 is not None:
    print(common_1)
    print(common_2)

    common = ""
    for i in range(len(common_1)):
        if common_1[i] == common_2[i]:
            common += common_1[i]
    print(common)

end = time.time()

# Part 2 Method 2
# More obvious method of just brute-forcing through the list
start_2 = time.time()

input_file = open('2018_2_input.txt', 'r').read().splitlines()
common_1 = None
common_2 = None
line_index = 0
while common_1 is None and line_index < len(input_file):
    line = input_file[line_index]
    for index_2 in range(line_index - 1):
        differences = 0
        line_2 = input_file[index_2]
        for letter_index in range(len(line)):
            if line[letter_index] != line_2[letter_index]:
                differences += 1
                if differences > 1:
                    break
        if differences < 2:
            common_1 = line
            common_2 = line_2
    line_index += 1

if common_1 is not None:
    print(common_1)
    print(common_2)

    common = ""
    for i in range(len(common_1)):
        if common_1[i] == common_2[i]:
            common += common_1[i]
    print(common)

end_2 = time.time()

print('First function timer:', end-start)
print('Second function timer:', end_2-start_2)
