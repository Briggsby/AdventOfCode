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


class Day12(Puzzle, day=12):
    def parse_nodes(self, lines: typing.Iterator[str]):
        Node.nodes = dict()
        target = None
        start = None
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "S":
                    start = Node(x, y, 0)
                elif char == "E":
                    target = Node(x, y, 25)
                else:
                    Node(x, y, self.convert_height(char))

        if target is None:
            raise ValueError("No target found")
        if start is None:
            raise ValueError("No start found")

        return start, target

    def solve_part_1(self, lines: typing.Iterator[str]):
        start, target = self.parse_nodes(lines)
        print(start.a_star_search(target, 1))

    @staticmethod
    def convert_height(height: str):
        lower_height = height.lower()
        base_height = ord(height) - 97
        return base_height if lower_height == height else base_height + 26

    def solve_part_2(self, lines: typing.Iterator[str]):
        start, target = self.parse_nodes(lines)
        shortest_path = start.a_star_search(target, 1)
        for node in Node.nodes.values():
            if node.height != 0 or node == start:
                continue
            try:
                shortest_path = min(node.a_star_search(target, 1), shortest_path)
            except ValueError as exc:
                if str(exc) != "No path found":
                    raise exc
        print(shortest_path)


if __name__ == "__main__":
    puzzle = Day12()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
