class Score:
    def __init__(self, score, index):
        self.score = score
        self.index = index
        self.left = None
        self.right = None

    def assign(self, left, right):
        self.left = left
        self.right = right
        left.right = self
        right.left = self

    def get_right_loop(self, index):
        if index == 0:
            return self
        else:
            return self.right.get_right_loop(index-1)

    def get_right(self, index):
        if index == 0:
            return self
        else:
            return self.right.get_right(index-1)

    def get_left(self, index):
        if index == 0:
            return self
        else:
            return self.left.get_left(index-1)

    def check_sequence(self, sequence):
        match = True
        for i in range(len(sequence)):
            if self.get_right(i).score != int(sequence[i]):
                match = False
                break
        return match


def new_scores(elf_1, elf_2, beginning, end, sequence, test_sequence):
    sum_score = elf_1.score + elf_2.score
    for digit in str(sum_score):
        new = Score(int(digit), end.index + 1)
        new.assign(end, beginning)
        test_sequence = test_sequence[1:] + str(new.score)
        if test_sequence == sequence:
            print(new.index-6)
        end = new
    return end, test_sequence


def new_scores_no_test(elf_1, elf_2, beginning, end, sequence):
    sum_score = elf_1.score + elf_2.score
    for digit in str(sum_score):
        new = Score(int(digit), end.index + 1)
        new.assign(end, beginning)
        end = new
    return end

# sequence = '59414'
# test_sequence = '71010'
# beginning = Score(3, 1)
# end = Score(7, 2)
# end.assign(beginning, beginning)
# elf_1 = beginning
# elf_2 = end
# for i in range(3):
#     end = new_scores_no_test(elf_1, elf_2, beginning, end, sequence)
#     elf_1 = elf_1.get_right_loop(elf_1.score+1)
#     elf_2 = elf_2.get_right_loop(elf_2.score+1)
# while True:
#     end, test_sequence = new_scores(elf_1, elf_2, beginning, end, sequence, test_sequence)
#     elf_1 = elf_1.get_right_loop(elf_1.score + 1)
#     elf_2 = elf_2.get_right_loop(elf_2.score + 1)


def new_score(scores, elf_1, elf_2, test_sequence, sequence):
    sum_score = scores[elf_1] + scores[elf_2]
    if sum_score < 10:
        scores.append(sum_score)
        test_sequence = test_sequence[1:] + str(sum_score)
        if test_sequence == sequence:
            print(len(scores))
    else:
        scores.append(1)
        test_sequence = test_sequence[1:] + str(1)
        if test_sequence == sequence:
            print(len(scores))
        scores.append(sum_score-10)
        test_sequence = test_sequence[1:] + str(sum_score-10)
        if test_sequence == sequence:
            print(len(scores))
    elf_1 = (elf_1 + scores[elf_1]+1) % len(scores)
    elf_2 = (elf_2 + scores[elf_2]+1) % len(scores)
    return scores, elf_1, elf_2, test_sequence


scores = [3, 7, 1, 0, 1, 0]
test_sequence = '371010'
sequence = '509671'
elf_1 = 3
elf_2 = 4
while True:
    scores, elf_1, elf_2, test_sequence = new_score(scores, elf_1, elf_2, test_sequence, sequence)
