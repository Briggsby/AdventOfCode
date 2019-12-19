input_file = open('2018_5_input.txt', 'r').read().splitlines()
polymer = input_file[0]
start = 1
done = False
while not done:
    for i in range(start, len(polymer)):
        if polymer[i-1].lower() == polymer[i].lower():
            if polymer[i-1] != polymer[i]:
                polymer = polymer[:i-1] + polymer[i+1:]
                start = max(1, i-2)
                break
        if i == len(polymer) - 1:
            done = True
print(polymer)
print(len(polymer))

# Part 2
input_file = open('2018_5_input.txt', 'r').read().splitlines()
base_polymer = input_file[0]
unit_types = set(base_polymer.lower())
unit_type_score = {}
lowest_score = len(polymer)
lowest_unit_type = ''
for removed_char in unit_types:
    polymer = base_polymer.replace(removed_char, '')
    polymer = polymer.replace(removed_char.upper(), '')
    start = 1
    done = False
    while not done:
        for i in range(start, len(polymer)):
            if polymer[i - 1].lower() == polymer[i].lower():
                if polymer[i - 1] != polymer[i]:
                    polymer = polymer[:i - 1] + polymer[i + 1:]
                    start = max(1, i - 2)
                    break
            if i == len(polymer) - 1:
                done = True
    unit_type_score[removed_char] = len(polymer)
    if len(polymer) < lowest_score:
        lowest_score = len(polymer)
        lowest_unit_type = removed_char
print(unit_type_score)
print(lowest_unit_type)
print(lowest_score)
