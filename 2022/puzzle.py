import abc
import typing


class Puzzle(abc.ABC):
    year: int = 2022
    day: int

    def __init_subclass__(cls, day: int):  # noqa
        cls.day = day

    @abc.abstractmethod
    def solve_part_1(self, lines: typing.Iterable[str]):
        pass

    @abc.abstractmethod
    def solve_part_2(self, lines: typing.Iterable[str]):
        pass

    def solve(self, part: int, test: bool):
        if part == 1:
            self.solve_part_1(self.get_input(test))
        elif part == 2:
            self.solve_part_2(self.get_input(test))

    def get_input(self, test: bool) -> typing.Generator[str, None, None]:
        with open(f"2022_{self.day}_{'test' if test else 'input'}.txt") as f:
            for line in f.readlines():
                yield line.rstrip("\n")
