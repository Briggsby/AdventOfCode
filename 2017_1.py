def puzzle_sum(numbers, halfway=False):
    result = 0
    n = len(numbers)
    plus = 1
    if halfway:
        plus = int(n/2)
    for i in range(n):
        if numbers[i] == numbers[(i+plus) % n]:
            result += numbers[i]
    return result


def convert_to_numbers(numbers):
    result = []
    app = result.append
    for n in numbers:
        try:
            app(int(n))
        except:
            pass
    return result


puzzle_input = open('2018_1_input.txt', 'r').read()
puzzle_input = convert_to_numbers(puzzle_input)
print(puzzle_sum(puzzle_input, True))
