import typing

from puzzle import Puzzle


class Day10(Puzzle, day=10):
    IMPORTANT_CYCLES = [20, 60, 100, 140, 180, 220]

    def solve_part_1(self, lines: typing.Iterator[str]):
        register = 1
        in_progress = False
        total = 0
        line = next(lines)
        for cycle in range(1, 221):
            if cycle in self.IMPORTANT_CYCLES:
                total += register * cycle

            if in_progress:
                register += int(line.split(" ")[1])
                in_progress = False
                line = next(lines)
                continue
            elif line == "noop":
                line = next(lines)
                continue
            else:
                in_progress = True
                continue

        print(total)


    CRT_WIDTH = 40

    def solve_part_2(self, lines: typing.Iterator[str]):
        register = 1
        in_progress = False
        line = next(lines)
        cycle = 0
        while True:
            cycle += 1

            if abs(register - (cycle % self.CRT_WIDTH)) <= 1:
                print("#", end="")
            else:
                print(".", end="")

            if cycle % self.CRT_WIDTH == 0:
                print("")

            if in_progress:
                register += int(line.split(" ")[1])
                in_progress = False
                try:
                    line = next(lines)
                except StopIteration:
                    break
                continue
            elif line == "noop":
                try:
                    line = next(lines)
                except StopIteration:
                    break
                continue
            else:
                in_progress = True
                continue


if __name__ == "__main__":
    puzzle = Day10()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
