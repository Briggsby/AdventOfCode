import typing

from puzzle import Puzzle

ROCK = 1
PAPER = 2
SCISSORS = 3

LOSE = 0
DRAW = 1
WIN = 2


class Day2(Puzzle, day=2):
    POINTS = {
        ROCK: 1,
        PAPER: 2,
        SCISSORS: 3,
    }
    WINS = {
        ROCK: SCISSORS,
        PAPER: ROCK,
        SCISSORS: PAPER,
    }
    LOSES = {value: key for key, value in WINS.items()}
    CODE = {
        "A": ROCK,
        "B": PAPER,
        "C": SCISSORS,
        "X": ROCK,
        "Y": PAPER,
        "Z": SCISSORS,
    }
    CODE_2 = {
        "X": LOSE,
        "Y": DRAW,
        "Z": WIN,
    }

    def solve_part_1(self, lines: typing.Iterable[str]):
        total_score = 0
        for line in lines:
            if line == "":
                continue
            opponent_code = line.split(" ")[0]
            player_code = line.split(" ")[1]
            result = self.points_per_round(
                self.CODE[opponent_code],
                self.CODE[player_code]
            )
            total_score += result
        print(total_score)

    def solve_part_2(self, lines: typing.Iterable[str]):
        total_score = 0
        for line in lines:
            if line == "":
                continue
            opponent_code = line.split(" ")[0]
            result_code = line.split(" ")[1]
            result = self.points_per_round_2(
                self.CODE[opponent_code],
                self.CODE_2[result_code]
            )
            total_score += result
        print(total_score)

    def points_per_round(self, opponent: int, player: int):
        if opponent == player:
            return 3 + self.POINTS[player]
        elif self.WINS[opponent] == player:
            return 0 + self.POINTS[player]
        elif self.WINS[player] == opponent:
            return 6 + self.POINTS[player]
        else:
            raise ValueError("Impossible result")

    def points_per_round_2(self, opponent: int, outcome: int):
        if outcome == LOSE:
            return 0 + self.POINTS[self.WINS[opponent]]
        elif outcome == DRAW:
            return 3 + self.POINTS[opponent]
        elif outcome == WIN:
            return 6 + self.POINTS[self.LOSES[opponent]]
        else:
            raise ValueError("Impossible result")


if __name__ == "__main__":
    puzzle = Day2()
    puzzle.solve(1, test=True)
    puzzle.solve(2, test=True)
    puzzle.solve(1, test=False)
    puzzle.solve(2, test=False)
