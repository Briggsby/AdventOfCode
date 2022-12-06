import typing

from puzzle import Puzzle


ITEMS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Day3(Puzzle, day=3):
    def solve_part_1(self, lines: typing.Iterable[str]):
        total = 0
        for line in lines:
            total += self.get_repeated_item_priority(line)
        print(total)

    def solve_part_2(self, lines: typing.Iterable[str]):
        total = 0
        lines = list(lines)
        line_count = 0
        while line_count <= (len(lines) - 3):
            total += self.get_repeated_item_priority_2(
                lines[line_count:(line_count+3)]
            )
            line_count += 3
        print(total)

    def get_repeated_item_priority(self, contents: str):
        first = set(contents[:(len(contents) // 2)])
        second = set(contents[(len(contents) // 2):])
        for index, item in enumerate(ITEMS):
            if item in first and item in second:
                return index + 1
        raise ValueError("No repeated item")

    def get_repeated_item_priority_2(self, contents: typing.List[str]):
        for index, item in enumerate(ITEMS):
            item_in_all = True
            for rucksack in contents:
                if item not in rucksack:
                    item_in_all = False
                    break
            if item_in_all:
                print(item, index + 1)
                return index + 1
        raise ValueError("No repeated badge")


if __name__ == "__main__":
    puzzle = Day3()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
