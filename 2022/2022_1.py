import typing
from functools import reduce

from puzzle import Puzzle


class Day1(Puzzle, day=1):
    NUMBER_TO_TRACK = 3

    def __init__(self):
        self.max_elf = 0
        self.max_elves = []

    def solve_part_1(self, lines: typing.Iterable[str]):
        self.max_elf = 0
        end = reduce(
            lambda current, line: (
                self.track_elf(current)
                if line == ""
                else current + int(line)
            ),
            lines,
            0,
        )
        self.track_elf(end)
        print(self.max_elf)

    def track_elf(self, calories):
        if calories > self.max_elf:
            self.max_elf = calories
        return 0

    def solve_part_2(self, lines: typing.Iterable[str]):
        self.max_elves = []
        end = reduce(
            lambda current, line: (
                self.track_elf_2(current)
                if line == ""
                else current + int(line)
            ),
            lines,
            0,
        )
        self.track_elf_2(end)
        print(sum(self.max_elves))

    def track_elf_2(self, calories):
        if len(self.max_elves) < self.NUMBER_TO_TRACK:
            self.max_elves.append(calories)

        smallest_chonky_elf = min(self.max_elves)
        if calories > smallest_chonky_elf:
            self.max_elves.remove(smallest_chonky_elf)
            self.max_elves.append(calories)

        return 0


if __name__ == "__main__":
    puzzle = Day1()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
