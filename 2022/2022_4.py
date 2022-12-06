import typing

from puzzle import Puzzle


class Day4(Puzzle, day=4):
    def solve_part_1(self, lines: typing.Iterable[str]):
        count = 0
        for line in lines:
            left = line.split(",")[0].split("-")
            right = line.split(",")[1].split("-")
            if self.pair_contains_other(
                    int(left[0]),
                    int(left[1]),
                    int(right[0]),
                    int(right[1])
            ):
                print(left, right)
                count += 1
        print(count)

    def solve_part_2(self, lines: typing.Iterable[str]):
        count = 0
        for line in lines:
            left = line.split(",")[0].split("-")
            right = line.split(",")[1].split("-")
            if self.pairs_overlap(
                    int(left[0]),
                    int(left[1]),
                    int(right[0]),
                    int(right[1])
            ):
                print(left, right)
                count += 1
        print(count)

    def pair_contains_other(
        self,
        min_left: int,
        max_left: int,
        min_right: int,
        max_right: int,
    ):
        if min_left >= min_right and max_left <= max_right:
            return True
        elif min_right >= min_left and max_right <= max_left:
            return True
        return False

    def pairs_overlap(
        self,
        min_left: int,
        max_left: int,
        min_right: int,
        max_right: int,
    ):
        if max(min_left, min_right) > min(max_left, max_right):
            return False
        return True


if __name__ == "__main__":
    puzzle = Day4()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
