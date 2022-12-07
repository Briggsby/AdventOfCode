import re
import typing
from collections import defaultdict, deque

from puzzle import Puzzle


class Day5(Puzzle, day=5):
    INSTRUCTION = re.compile(r"move (\d+) from (\d+) to (\d+)")

    def solve_part_1(self, lines: typing.Iterator[str]):
        stacks = self.parse_stacks(lines)
        for line in lines:
            if line == "":
                continue
            match = self.INSTRUCTION.fullmatch(line)
            stacks[int(match.groups()[2])].extend(
                stacks[int(match.groups()[1])].pop()
                for _ in range(int(match.groups()[0]))
            )
        for key in sorted(stacks.keys()):
            print(stacks[key].pop(), end="")
        print()

    def solve_part_2(self, lines: typing.Iterator[str]):
        stacks = self.parse_stacks(lines)
        for line in lines:
            if line == "":
                continue
            match = self.INSTRUCTION.fullmatch(line)
            stacks[int(match.groups()[2])].extend(reversed([
                stacks[int(match.groups()[1])].pop()
                for _ in range(int(match.groups()[0]))
            ]))
        for key in sorted(stacks.keys()):
            print(stacks[key].pop(), end="")
        print()

    def parse_stacks(self, lines):
        piles = defaultdict(list)
        for line in lines:
            if line[1] == '1':
                break
            index = 1
            while index < len(line):
                if line[index] != ' ':
                    piles[(index // 4) + 1].append(line[index])
                index += 4
        stacks = {}
        for key, value in piles.items():
            stacks[key] = deque(reversed(value))
        return stacks


if __name__ == "__main__":
    puzzle = Day5()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
