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


def new_scores(elf_1, elf_2, beginning, end, sequence):
    sum_score = elf_1.score + elf_2.score
    for digit in str(sum_score):
        new = Score(int(digit), end.index + 1)
        new.assign(end, beginning)
        if new.score == int(sequence[len(sequence)-1]):
            if new.get_left(len(sequence)-1).check_sequence(sequence):
                print(new.get_left(len(sequence)-1).index-1)
        end = new
    return end


sequence = '509671'
beginning = Score(3, 1)
end = Score(7, 2)
end.assign(beginning, beginning)
elf_1 = beginning
elf_2 = end
for i in range(3):
    end = new_scores(elf_1, elf_2, beginning, end, sequence)
    elf_1 = elf_1.get_right_loop(elf_1.score+1)
    elf_2 = elf_2.get_right_loop(elf_2.score+1)
while True:
    end = new_scores(elf_1, elf_2, beginning, end, sequence)
    elf_1 = elf_1.get_right_loop(elf_1.score + 1)
    elf_2 = elf_2.get_right_loop(elf_2.score + 1)
