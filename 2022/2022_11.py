import dataclasses
import re
import typing
from collections import deque

from puzzle import Puzzle


@dataclasses.dataclass
class Item:
    holder: int
    worry_level: int

    worry_level_modulos: dict[int, int] = dataclasses.field(init=False)

    def __post_init__(self):
        Monkey.get_monkey(self.holder).items.append(self)
        self.worry_level_modulos = dict()

    def split_worry_levels(self, bases: typing.List[int]):
        self.worry_level_modulos = {
            base: self.worry_level % base
            for base in bases
        }


class Monkey:
    monkeys = dict()
    relief: int = 3

    index: int
    items: typing.Deque[Item]
    operator: str
    test: int

    true_throw_target: int
    false_throw_target: int

    def __init__(self, index):
        Monkey.monkeys[index] = self
        self.index = index
        self.items = deque()
        self.items_inspected = 0

    def __repr__(self):
        return (
            f"Monkey {self.index}, "
            f"items: {[item.worry_level_modulos for item in self.items]}"
        )

    def test_item(self, item):
        if self.relief != 1:
            return item.worry_level % self.test == 0

        return item.worry_level_modulos[self.test] % self.test == 0

    @classmethod
    def get_monkey(cls, index):
        return cls.monkeys.get(index) or Monkey(index)

    def operate(self, item):
        if self.relief != 1:
            old = item.worry_level  # noqa
            new = eval(self.operator) // self.relief
            item.worry_level = new
            return

        for base, value in item.worry_level_modulos.items():
            old = item.worry_level_modulos[base]  # noqa
            new = eval(self.operator) // self.relief
            item.worry_level_modulos[base] = new % base

    def take_turn(self):
        while len(self.items) > 0:
            self.inspect_item()

    def inspect_item(self):
        item = self.items.popleft()
        self.operate(item)
        target = (
            self.true_throw_target
            if self.test_item(item)
            else self.false_throw_target
        )

        item.holder = target
        Monkey.get_monkey(target).items.append(item)

        self.items_inspected += 1


class Day11(Puzzle, day=11):
    MONKEY_PATTERN = re.compile(r"Monkey (?P<index>\d+):")
    ITEMS_PATTERN = re.compile(r"\s+Starting items: (?P<items>.*)")
    OPERATION_PATTERN = re.compile(
        r"\s+Operation: new = (?P<expression>old [*+] (old|\d+))"
    )
    TEST_PATTERN = re.compile(r"\s+Test: divisible by (?P<amount>\d+)")
    IF_TRUE_PATTERN = re.compile(r"\s+If true: throw to monkey (?P<index>\d+)")
    IF_FALSE_PATTERN = re.compile(
        r"\s+If false: throw to monkey (?P<index>\d+)"
    )

    def parse_monkeys(self, lines: typing.Iterator[str]):
        Monkey.monkeys = dict()
        current_monkey = None
        bases = set()
        for line in lines:
            if match := self.MONKEY_PATTERN.match(line):
                current_monkey = int(match.groupdict()["index"])
            elif match := self.ITEMS_PATTERN.match(line):
                items = match.groupdict()["items"].split(",")
                for item in items:
                    Item(current_monkey, int(item))
            elif match := self.OPERATION_PATTERN.match(line):
                expression = match.groupdict()["expression"]
                Monkey.get_monkey(current_monkey).operator = expression
            elif match := self.TEST_PATTERN.match(line):
                amount = int(match.groupdict()["amount"])
                bases.add(amount)
                Monkey.get_monkey(current_monkey).test = amount
            elif match := self.IF_TRUE_PATTERN.match(line):
                target = int(match.groupdict()["index"])
                Monkey.get_monkey(current_monkey).true_throw_target = target
            elif match := self.IF_FALSE_PATTERN.match(line):
                target = int(match.groupdict()["index"])
                Monkey.get_monkey(current_monkey).false_throw_target = target

        for monkey in Monkey.monkeys.values():
            for item in monkey.items:
                item.split_worry_levels(bases)

        return current_monkey

    def solve_part_1(self, lines: typing.Iterator[str]):
        Monkey.relief = 3
        max_monkey = self.parse_monkeys(lines)

        for _round in range(20):
            for monkey in range(max_monkey + 1):
                Monkey.get_monkey(monkey).take_turn()
            # print(f"Round {_round}")
            # for monkey in Monkey.monkeys.values():
            #     print(monkey)

        for monkey in Monkey.monkeys.values():
            print(monkey)

        monkey_activity = sorted(
            [monkey for monkey in Monkey.monkeys.values()],
            key=lambda monkey: monkey.items_inspected,
            reverse=True,
        )
        print(
            monkey_activity[0].items_inspected
            * monkey_activity[1].items_inspected
        )

    def solve_part_2(self, lines: typing.Iterator[str]):
        Monkey.relief = 1
        max_monkey = self.parse_monkeys(lines)
        for _round in range(10000):
            for monkey in range(max_monkey + 1):
                Monkey.get_monkey(monkey).take_turn()
            # if _round + 1 in (1, 20) or (_round + 1) % 1000 == 0:
            #     print(f"Round {_round + 1}")
            #     for monkey in Monkey.monkeys.values():
            #         print(monkey.items_inspected)
        monkey_activity = sorted(
            [monkey for monkey in Monkey.monkeys.values()],
            key=lambda monkey: monkey.items_inspected,
            reverse=True,
        )
        print(
            monkey_activity[0].items_inspected
            * monkey_activity[1].items_inspected
        )


if __name__ == "__main__":
    puzzle = Day11()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
