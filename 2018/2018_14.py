class Score:
    def __init__(self, score, left, right, index):
        self.score = score
        self.left = left
        self.right = right
        self.index = index
        if left is not None and right is not None:
            self.left.right = self
            self.right.left = self

    def get_right(self, amount, loop=True):
        if amount == 0:
            return self
        elif amount == 1:
            if not loop and self.right.index < self.index:
                return None
            else:
                return self.right
        else:
            if not loop and self.right.index < self.index:
                return None
            else:
                return self.right.get_right(amount-1, loop)

    def get_left(self, amount, loop=True):
        if amount == 0:
            return self
        elif amount == 1:
            if not loop and self.left.index > self.index:
                return None
            else:
                return self.left
        else:
            if not loop and self.left.index > self.index:
                return None
            else:
                return self.left.get_left(amount-1, loop)

    def get_index(self, index):
        if self.index == index:
            return self
        elif self.index > index:
            return self.left.get_index(index)
        else:
            return self.right.get_index(index)

    def get_sequence(self, length):
        if length == 1:
            return str(self.score)
        return str(self.score)+self.right.get_sequence(length-1)


def new_recipes(elves, beginning_score, end_score):
    sum_score = 0
    for elf in elves:
        sum_score += elf.score
    for digit in str(sum_score):
        end_score = Score(int(digit), end_score, beginning_score, end_score.index+1)
    return end_score


def new_recipes_part_2(elves, beginning_score, end_score, solution):
    sum_score = 0
    original_end_score = end_score
    for elf in elves:
        sum_score += elf.score
    for digit in str(sum_score):
        end_score = Score(int(digit), end_score, beginning_score, end_score.index + 1)
    solution = str(solution)
    digits = len(solution)
    current_score = original_end_score.get_left(digits-2, False)
    matched_score = None
    while current_score is not None and end_score.index-current_score.index >= digits-1:
        match_check = current_score.get_sequence(digits)
        if match_check == solution:
            matched_score = current_score
        current_score = current_score.right
    return end_score, matched_score


def pick_new_score(score):
    return score.get_right(score.score+1)


def pick_new_scores(elves):
    for i in range(len(elves)):
        elves[i] = pick_new_score(elves[i])
    return elves


def print_scores(beginning_score, end_score, elves):
    current_score = beginning_score
    while True:
        if current_score in elves:
            print('[', current_score.score, ']', sep='', end='')
        else:
            print(' ', current_score.score, sep='', end=' ')
        if current_score is end_score:
            break
        current_score = current_score.right
    print()


def part_1(number, print_last):
    elves = [None, None]
    elves[0] = Score(3, None, None, 1)
    elves[1] = Score(7, elves[0], elves[0], 2)
    beginning = elves[0]
    end = elves[1]
    print_scores(beginning, end, elves)
    while end.index < number+print_last:
        end = new_recipes(elves, beginning, end)
        elves = pick_new_scores(elves)
        # print_scores(beginning, end, elves)
    end = end.get_index(number+print_last)
    print_scores(end.get_left(print_last-1), end, elves)


def part_2(number, limit=9999999):
    elves = [None, None]
    elves[0] = Score(3, None, None, 1)
    elves[1] = Score(7, elves[0], elves[0], 2)
    beginning = elves[0]
    end = elves[1]
    print_scores(beginning, end, elves)
    n = 0
    while True and n < limit:
        end, matched = new_recipes_part_2(elves, beginning, end, number)
        if matched is not None:
            break
        elves = pick_new_scores(elves)
        # print_scores(beginning, end, elves)
        n += 1
    print_scores(beginning, end, elves)
    print(matched.index-1)


part_1(509671, 10)
part_2('509671')
