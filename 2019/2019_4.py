min_combination = 372037
max_combination = 905157

def combination_checker(number):
    prev_char = 0
    adjacency = False
    for char in str(number):
        if int(char) < int(prev_char):
            return False
        if char == prev_char:
            adjacency = True
        prev_char = char
    return adjacency

print(combination_checker(111111))
print(combination_checker(223450))
print(combination_checker(123789))


matches = []
for i in range(min_combination, max_combination+1):
    if combination_checker(i):
        matches.append(i)
print(len(matches))


def part2_combination_checker(number):
    prev_char = 0
    adjacency = False
    chain = False
    for i in range(len(str(number))):
        char = str(number)[i]
        if int(char) < int(prev_char):
            return False
        if char == prev_char:
            if not chain:
                next_char = str(number)[i+1] if i+1 < len(str(number)) else None
                if next_char == char:
                    chain = True
                else:
                    adjacency = True
        elif chain:
            chain = False
        prev_char = char
    return adjacency

print(part2_combination_checker(112233))
print(part2_combination_checker(123444))
print(part2_combination_checker(111122))

matches_2 = []
for i in range(min_combination, max_combination+1):
    if part2_combination_checker(i):
        matches_2.append(i)
print(len(matches_2))