import typing

from puzzle import Puzzle

START = (0, 0)
MAPPING = {
    "R": (1, 0),
    "U": (0, 1),
    "L": (-1, 0),
    "D": (0, -1),
}


class Day9(Puzzle, day=9):
    def add_vector(self, vector_1, vector_2):
        return vector_1[0] + vector_2[0], vector_1[1] + vector_2[1]

    def get_tail_movement(self, head_position, tail_position):
        if max(
            abs(head_position[0] - tail_position[0]),
            abs(head_position[1] - tail_position[1])
        ) <= 1:
            return tail_position
        elif head_position[1] == tail_position[1]:
            direction = 1 if head_position[0] > tail_position[0] else -1
            return tail_position[0] + direction, tail_position[1]
        elif head_position[0] == tail_position[0]:
            direction = 1 if head_position[1] > tail_position[1] else -1
            return tail_position[0], tail_position[1] + direction
        else:
            x_direction = 1 if head_position[0] > tail_position[0] else -1
            y_direction = 1 if head_position[1] > tail_position[1] else -1
            return tail_position[0] + x_direction, tail_position[1] + y_direction

    def solve_part_1(self,  lines: typing.Iterator[str]):
        head_position = START
        tail_position = START
        tail_positions = {START}
        for line in lines:
            direction = line.split(" ")[0]
            magnitude = int(line.split(" ")[1])
            for _ in range(magnitude):
                head_position = self.add_vector(head_position, MAPPING[direction])
                tail_position = self.get_tail_movement(head_position, tail_position)
                tail_positions.add(tail_position)
        print(tail_positions)
        print(len(tail_positions))

    def solve_part_2(self, lines: typing.Iterator[str]):
        knot_positions = [START] * 10
        tail_positions = {START}
        for line in lines:
            direction = line.split(" ")[0]
            magnitude = int(line.split(" ")[1])
            for _ in range(magnitude):
                knot_positions[0] = self.add_vector(knot_positions[0], MAPPING[direction])
                for index in range(1, len(knot_positions)):
                    knot_positions[index] = self.get_tail_movement(
                        knot_positions[index - 1],
                        knot_positions[index]
                    )
                tail_positions.add(knot_positions[9])
        print(tail_positions)
        print(len(tail_positions))


if __name__ == "__main__":
    puzzle = Day9()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
