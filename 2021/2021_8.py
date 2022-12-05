from collections import defaultdict
from typing import List

numbers = {
    0: ('a', 'b', 'c', 'e', 'f', 'g'),
    1: ('c', 'f'),
    2: ('a', 'c', 'd', 'e', 'g'),
    3: ('a', 'c', 'd', 'f', 'g'),
    4: ('b', 'c', 'd', 'f'),
    5: ('a', 'b', 'd', 'f', 'g'),
    6: ('a', 'b', 'd', 'e', 'f', 'g'),
    7: ('a', 'c', 'f'),
    8: ('a', 'b', 'c', 'd', 'e', 'f', 'g'),
    9: ('a', 'b', 'c', 'd', 'f', 'g'),
}

numbers_by_length = {
    2: (1),
    3: (7),
    4: (4),
    5: (2, 3, 5),
    6: (0, 6, 9),
    7: (8),
}

def find_true_mappings(patterns: List[str]):
    # Each pattern is a list of characters
    # Each character corresponds to a character in numbers ('a' -> 'g')
    # We need to work out which is which

    # For each pattern in list we can know if it has to be one of possible
    # numbers by the length of the string

    # Then we can limit each character to have to be one of the characters
    # in those numbers

    possible_mappings = defaultdict(set)

    for pattern in patterns:
        for number in numbers_by_length[len(pattern)]:
            pass


test_input = open('./2021_8_test.txt', 'r').read().splitlines()
puzzle_input = open('./2021_8_input.txt', 'r').read().splitlines()

count = 0
for line in puzzle_input:
    output = line.split(' | ')[1]
    output_patterns = output.split(' ')
    for pattern in output_patterns:
        count += 1 if len(pattern) in (2, 3, 4, 7) else 0

print(count)
