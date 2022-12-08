import typing

from puzzle import Puzzle

DIFFERENT_CHARS = 4
DIFFERENT_CHARS_2 = 14


class Day6(Puzzle, day=6):

    def solve_part_1(self,  lines: typing.Iterator[str]):
        line = next(lines)
        chars = []
        for index, char in enumerate(line):
            if (
                    len(chars) == DIFFERENT_CHARS - 1
                    and len(set(chars)) == DIFFERENT_CHARS - 1
                    and char not in chars
            ):
                print(chars + [char])
                print(index + 1)
                return
            elif len(chars) == DIFFERENT_CHARS - 1:
                chars.pop(0)
            chars.append(char)

    def solve_part_2(self, lines: typing.Iterator[str]):
        line = next(lines)
        chars = []
        for index, char in enumerate(line):
            if (
                    len(chars) == DIFFERENT_CHARS_2 - 1
                    and len(set(chars)) == DIFFERENT_CHARS_2 - 1
                    and char not in chars
            ):
                print(chars + [char])
                print(index + 1)
                return
            elif len(chars) == DIFFERENT_CHARS_2 - 1:
                chars.pop(0)
            chars.append(char)


if __name__ == "__main__":
    puzzle = Day6()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
