import functools
import typing
from typing import Dict, Tuple, Optional

from puzzle import Puzzle


class Node:
    nodes: Dict[Tuple[int, int], "Node"] = dict()

    x: int
    y: int
    height: int

    f: Optional[int]
    g: Optional[int]
    h: Optional[int]

    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height

        self.f = None
        self.g = None
        self.h = None

        Node.nodes[(x, y)] = self

    def __repr__(self):
        return f"Node {self.x}, {self.y}, {self.height}"

    def get_neighbors(self):
        return [node for node in [
            self.nodes.get((self.x + 1, self.y)),
            self.nodes.get((self.x - 1, self.y)),
            self.nodes.get((self.x, self.y + 1)),
            self.nodes.get((self.x, self.y - 1)),
        ] if node is not None
        ]

    def get_neighbors_within_height_diff(self, max_difference: int):
        return (
            node for node in self.get_neighbors()
            if (node.height - self.height) <= max_difference
        )

    def a_star_search(self, target: "Node", max_difference: int):
        for node in self.nodes.values():
            node.f = None
            node.g = None
            node.h = abs(node.x - self.x) + abs(node.y - self.y)

        self.g = 0
        self.f = 0
        open_list = {self}
        closed_list = {self}
        while len(open_list) > 0:
            current_node: Optional["Node"] = None
            for node in open_list:
                if current_node is None or current_node.f > node.f:
                    current_node = node

            open_list.remove(current_node)
            closed_list.add(current_node)

            if current_node == target:
                return current_node.g

            for node in current_node.get_neighbors_within_height_diff(
                    max_difference
            ):
                if node in closed_list:
                    continue
                elif node in open_list:
                    node.g = min(current_node.g + 1, node.g)
                    node.f = node.g + node.h
                else:
                    open_list.add(node)
                    node.g = current_node.g + 1
                    node.f = node.g + node.h

        raise ValueError("No path found")


RecursiveList = typing.Union[typing.List["RecursiveList"], int]


class Day13(Puzzle, day=13):
    def compare_values(
            self,
            left: RecursiveList,
            right: RecursiveList,
    ):
        if isinstance(left, int) and isinstance(right, int):
            return left < right
        if isinstance(left, int):
            left = [left]
        if isinstance(right, int):
            right = [right]

        for index in range(len(left)):
            if index >= len(right):
                return False

            left_item = left[index]
            right_item = right[index]
            if self.wrap_in_list(left_item) == self.wrap_in_list(right_item):
                continue

            return self.compare_values(left_item, right_item)

        return True

    def wrap_in_list(self, item):
        if isinstance(item, int):
            return [item]
        else:
            return item

    def compare_values_key_func(
            self,
            left: RecursiveList,
            right: RecursiveList,
    ):
        if left == right:
            return 0
        elif self.compare_values(left, right):
            return -1
        else:
            return +1

    def solve_part_1(self, lines: typing.Iterator[str]):
        total = 0
        for index, line in enumerate(lines):
            left = eval(line)
            right = eval(next(lines))
            if self.compare_values(left, right):
                total += index + 1
            next(lines, None)
        print(total)

    DIVIDER_1 = [[2]]
    DIVIDER_2 = [[6]]

    def solve_part_2(self, lines: typing.Iterator[str]):
        packets = (
            eval(line) for line in lines
            if line != ""
        )
        index_1 = 1
        index_2 = 2

        packets = list(packets)

        for packet in packets:
            if self.compare_values(packet, self.DIVIDER_1):
                index_1 += 1
            if self.compare_values(packet, self.DIVIDER_2):
                index_2 += 1

        print(index_1, index_2)
        print(index_1 * index_2)


if __name__ == "__main__":
    puzzle = Day13()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
