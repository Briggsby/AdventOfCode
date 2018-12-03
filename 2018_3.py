def get_vector(string):
    # returns x pos, y pos, width, length
    string = string.replace(',', ' ').replace(':', ' ').replace('x', ' ')
    parts = string.split(' ')
    vector_id = parts[0]
    vector = [int(parts[2]), int(parts[3]), int(parts[5]), int(parts[6])]
    return [vector_id, vector]


class Cut:
    vector = []
    id = str()
    x = int()
    y = int()
    x_delta = int()
    y_delta = int()
    x_plus = int()
    y_plus = int()

    def __init__(self, vector, vector_id):
        if vector is None:
            del self
            return
        self.id = vector_id
        self.vector = vector
        self.x = vector[0]
        self.y = vector[1]
        self.x_delta = vector[2]
        self.y_delta = vector[3]
        self.x_plus = self.x+self.x_delta
        self.y_plus = self.y+self.y_delta

    def top_left(self):
        return [self.x, self.y]

    def top_right(self):
        return [self.x_plus, self.y]

    def bottom_left(self):
        return [self.x, self.y_plus]

    def bottom_right(self):
        return [self.x_plus, self.y_plus]

    def get_overlap(self, other):
        # This clearly doesn't work right ,as we get two solutions to part 2
        x_overlap = None
        x_overlap_delta = None
        y_overlap = None
        y_overlap_delta = None
        if other.x <= self.x < other.x_plus:
            x_overlap = self.x
            x_overlap_delta = min(self.x_delta, other.x_plus-self.x)
        elif other.x < self.x_plus <= other.x_plus:
            x_overlap_delta = min(self.x_delta, self.x_plus-other.x)
            x_overlap = self.x_plus - x_overlap_delta
        elif self.x < other.x and self.x_plus > other.x_plus:
            x_overlap = other.x
            x_overlap_delta = other.x_delta
        elif other.x < self.x and other.x_plus > self.x_plus:
            x_overlap = self.x
            x_overlap_delta = self.x_delta
        if other.y <= self.y < other.y_plus:
            y_overlap = self.y
            y_overlap_delta = min(self.y_delta, other.y_plus-self.y)
        elif other.y < self.y_plus < other.y_plus:
            y_overlap_delta = min(self.y_delta, self.y_plus-other.y)
            y_overlap = self.y_plus - y_overlap_delta
        elif self.y < other.y and self.y_plus > other.y_plus:
            y_overlap = other.y
            y_overlap_delta = other.y_delta
        elif other.y < self.y and other.y_plus > self.y_plus:
            y_overlap = self.y
            y_overlap_delta = self.y_delta
        if x_overlap_delta and y_overlap_delta:
            return [x_overlap, y_overlap, x_overlap_delta, y_overlap_delta]

    def area(self):
        return self.x_delta*self.y_delta


input_file = open('2018_3_input.txt', 'r').read().splitlines()

# Method 1: Check coordinates
cut_vectors = [get_vector(line) for line in input_file]
cuts = [Cut(cut[1], cut[0]) for cut in cut_vectors]
sheet_width = max([cut.x_plus for cut in cuts])+1
sheet_height = max([cut.y_plus for cut in cuts])+1
print('Sheet dimensions:', sheet_width, sheet_height)
sheet = [0]*sheet_width*sheet_height  # Uncut = 0, cut = 1, double cut = 2


def get_coord(x, y):
    return sheet_width*y + x


def cut_sheet(x, y):
    coords = get_coord(x, y)
    if sheet[coords] == 0:
        sheet[coords] = 1
    else:
        sheet[coords] = 2


def cut_sheet_area(cut):
    for x in range(cut.x, cut.x_plus):
        for y in range(cut.y, cut.y_plus):
            cut_sheet(x, y)


def print_sheet():
    for n in range(len(sheet)):
        print(sheet[n], end='', flush=True)
        if n % sheet_width == 0:
            print()
    print()


for i in range(len(cuts)):
    cut_sheet_area(cuts[i])
# print_sheet()
print(sheet.count(2))


# Method 2: Compare cuts
# THIS DOES NOT WORK
# Because overlaps can overlap
# It's also much slower as of right now

def method_2():
    cuts = []
    double_cuts = []
    area = 0
    overlapped_doubles = 0

    for line in input_file:
        new_cut = Cut(get_vector(line))
        for cut in cuts:
            overlap = new_cut.get_overlap(cut)
            if overlap:
                new_double_cut = Cut(overlap)
                area += new_double_cut.area()
                for double_cut in double_cuts:
                    double_overlap = Cut(new_double_cut.get_overlap(double_cut))
                    if double_overlap:
                        overlapped_doubles += double_overlap.area()
                        area -= double_overlap.area()
                double_cuts.append(new_double_cut)
        cuts.append(new_cut)
    print(area)


# Part 2
# We actually get two solutions to part 2, so something isn't working right

for i in range(len(cuts)):
    no_overlap = True
    cut = cuts[i]
    for j in range(len(cuts)):
        other_cut = cuts[j]
        if i != j and cut.get_overlap(other_cut):
            no_overlap = False
            break
    if no_overlap:
        print(cuts[i].id)




