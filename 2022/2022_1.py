import typing

from puzzle import Puzzle


class Day1(Puzzle, day=1):

    def solve_part_1(self, lines: typing.Iterable[str]):
        elves = []
        max_calories = 0

        current_calories = 0
        for line in lines:
            if line == "":
                elves.append(current_calories)
                max_calories = max([current_calories, max_calories])
                current_calories = 0
            else:
                current_calories += int(line)
        elves.append(current_calories)
        max_calories = max([current_calories, max_calories])

        print(elves)
        print(max_calories)

    def solve_part_2(self, lines: typing.Iterable[str]):
        elves = []

        current_calories = 0
        for line in lines:
            if line == "":
                elves.append(current_calories)
                current_calories = 0
            else:
                current_calories += int(line)
        elves.append(current_calories)

        print(sum(sorted(elves, reverse=True)[:3]))


if __name__ == "__main__":
    puzzle = Day1()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
