def get_map(file):
    input_file = open(file, 'r').read().splitlines()
    return [[[get_type(i), 0] for i in line] for line in input_file]


def get_type(character):
    # Open: '.' / 0, Lumberyard: '#' / 1 Trees: '|' / 2
    if character == '.':
        return 0
    if character == '#':
        return 1
    else:
        return 2


def get_icon(number):
    # Open: '.' / 0, Lumberyard: '#' / 1 Trees: '|' / 2
    if number == 0:
        return '.'
    if number == 1:
        return '#'
    else:
        return '|'


def print_area(lumber_area):
    print("Open: '.' / 0, Lumberyard: '#' / 1 Trees: '|' / 2")
    for line in lumber_area:
        for number in line:
            print(get_icon(number[0]), end='')
        print()


def mutate(lumber_area):
    # Open: '.' / 0, Lumberyard: '#' / 1 Trees: '|' / 2
    y_range = len(lumber_area)
    x_range = len(lumber_area[0])
    for y in range(y_range):
        for x in range(x_range):
            if lumber_area[y][x][0] == 0:
                # Becomes trees if at least 3 adjacent areas are trees
                # Otherwise stays open
                lumber_area[y][x][1] = 0
                adjacent_woods = 0
                for x_delt in [-1, 0, 1]:
                    for y_delt in [-1, 0, 1]:
                        if (0 <= y+y_delt < y_range) and (0 <= x+x_delt < x_range) and not (x_delt == 0 and y_delt == 0):
                            if lumber_area[y+y_delt][x+x_delt][0] == 2:
                                adjacent_woods += 1
                if adjacent_woods >= 3:
                    lumber_area[y][x][1] = 2
            if lumber_area[y][x][0] == 1:
                # Stays lumber if at least one lumberyard and one trees adjacent
                # Otherwise becomes open
                lumber_area[y][x][1] = 0
                near_lumber = False
                near_trees = False
                for x_delt in [-1, 0, 1]:
                    for y_delt in [-1, 0, 1]:
                        if (0 <= y+y_delt < y_range) and (0 <= x+x_delt < x_range) and not (x_delt == 0 and y_delt == 0):
                            if lumber_area[y + y_delt][x + x_delt][0] == 2:
                                near_trees = True
                            if lumber_area[y+y_delt][x+x_delt][0] == 1:
                                near_lumber = True
                if near_lumber and near_trees:
                    lumber_area[y][x][1] = 1
            if lumber_area[y][x][0] == 2:
                # Becomes a lumberyard if three or more adjacent lumberyards
                # otherwise stays trees
                lumber_area[y][x][1] = 2
                adjacent_lumbers = 0
                for x_delt in [-1, 0, 1]:
                    for y_delt in [-1, 0, 1]:
                        if (0 <= y+y_delt < y_range) and (0 <= x+x_delt < x_range) and not (x_delt == 0 and y_delt == 0):
                            if lumber_area[y + y_delt][x + x_delt][0] == 1:
                                adjacent_lumbers += 1
                if adjacent_lumbers >= 3:
                    lumber_area[y][x][1] = 1
    for y in range(y_range):
        for x in range(x_range):
            lumber_area[y][x][0] = lumber_area[y][x][1]
    return lumber_area


area = get_map('2018_18_input.txt')
print_area(area)
for n in range(10000):
    area = mutate(area)
    # print_area(area)
    count = [0, 0, 0]
    for y in area:
        for x in y:
            count[x[0]] += 1
    print(n, ':', count)

