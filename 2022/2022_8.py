import functools
import itertools
import typing

from puzzle import Puzzle

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class Day8(Puzzle, day=8):
    def parse_input(self, lines):
        return [
            [int(digit) for digit in line]
            for line in lines
        ]

    def is_visible(self,
                   row_index: int,
                   column_index: int,
                   direction: int,
                   trees: typing.List[typing.List[int]],
                   visible_trees: typing.List[typing.List[typing.List[typing.Optional[bool]]]]
   ):
        """Incorrect function that returns is_visible if all trees in between edge and this tree are visible"""
        tree_height = trees[row_index][column_index]
        if visible_trees[row_index][column_index][direction] is not None:
            return visible_trees[row_index][column_index][direction]
        if direction == UP:
            visible = (
                row_index - 1 < 0
                or (trees[row_index - 1][column_index] < tree_height and self.is_visible(row_index - 1, column_index, direction,
                                                                                         trees, visible_trees))
            )
        elif direction == DOWN:
            visible = (
                row_index + 1 >= len(trees)
                or (trees[row_index + 1][column_index] < tree_height and self.is_visible(row_index + 1, column_index, direction,
                                                                                         trees, visible_trees))
            )
        elif direction == LEFT:
            visible = (
                column_index - 1 < 0
                or (trees[row_index][column_index - 1] < tree_height and self.is_visible(row_index, column_index - 1, direction,
                                                                                         trees, visible_trees))
            )
        elif direction == RIGHT:
            visible = (
                column_index + 1 >= len(trees[row_index])
                or (trees[row_index][column_index + 1] < tree_height and self.is_visible(row_index, column_index + 1, direction,
                                                                                         trees, visible_trees))
            )
        else:
            raise ValueError("Invalid Direction")
        visible_trees[row_index][column_index][direction] = visible
        return visible

    def solve_part_1(self,  lines: typing.Iterator[str]):
        trees = self.parse_input(lines)
        # visible_trees = [[[None, None, None, None] for _ in row] for row in trees]
        visibility = [[False for _ in row] for row in trees]
        visible_trees = 0
        for row_index, row in enumerate(trees):
            for column_index, tree in enumerate(row):
                visible = False
                if row_index == 0 or row_index == (len(trees) - 1):
                    visible = True
                elif column_index == 0 or column_index == (len(row) - 1):
                    visible = True
                elif max(trees[row_index][:column_index]) < tree:
                    visible = True
                elif max(trees[row_index][(column_index + 1):len(trees)]) < tree:
                    visible = True
                elif max([trees[i][column_index] for i in range(row_index)]) < tree:
                    visible = True
                elif max(trees[i][column_index] for i in range(row_index + 1, len(trees))) < tree:
                    visible = True

                visible_trees += 1 if visible else 0
                visibility[row_index][column_index] = visible
        for line in visibility:
            print(line)
        print(visible_trees)

    def solve_part_2(self, lines: typing.Iterator[str]):
        trees = self.parse_input(lines)
        # visible_trees = [[[None, None, None, None] for _ in row] for row in trees]
        scenic_scores = [[None for _ in row] for row in trees]
        highest_score = 0
        for row_index, row in enumerate(trees):
            for column_index, tree in enumerate(row):
                scenic_score = 1
                scenic_score *= next(
                    (index + 1 for index, item in enumerate(
                        trees[row_index][i] for i in range(column_index - 1, -1, -1)
                    ) if item >= tree or index == column_index - 1),
                    0,
                )
                scenic_score *= next(
                    (index + 1 for index, item in enumerate(
                        trees[row_index][i] for i in range(column_index + 1, len(row))
                    ) if item >= tree or (index + column_index) == (len(row) - 2)),
                    0,
                )
                scenic_score *= next(
                    (index + 1 for index, item in enumerate(
                        trees[i][column_index] for i in range((row_index - 1), -1, -1)
                    ) if item >= tree or index == row_index - 1),
                    0,
                )
                scenic_score *= next(
                    (index + 1 for index, item in enumerate(
                        trees[i][column_index] for i in range(row_index + 1, len(trees))
                    ) if item >= tree or index + row_index == len(trees) - 2),
                    0,
                )
                scenic_scores[row_index][column_index] = scenic_score
                highest_score = max([highest_score, scenic_score])
        for line in scenic_scores:
            print(line)
        print(highest_score)


if __name__ == "__main__":
    puzzle = Day8()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
