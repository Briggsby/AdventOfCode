import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_nanobots(file):
    lines = [line.split(', ') for line in open(file).read().splitlines()]
    nanobots = [[[int(i) for i in line[0][len('pos=<'):-1].split(',')], int(line[1][len('r='):])] for line in lines]
    return nanobots


def in_range(nano_1, nano_2):
    distance = sum([abs(nano_2[0][0]-nano_1[0][0]), abs(nano_2[0][1]-nano_1[0][1]), abs(nano_2[0][2]-nano_1[0][2])])
    radius = nano_1[1]
    if distance <= radius:
        return True
    else:
        return False


def in_range_pos(nano, pos):
    distance = sum([abs(nano[0][0] - pos[0]), abs(nano[0][1] - pos[1]), abs(nano[0][2] - pos[2])])
    radius = nano[1]
    if distance <= radius:
        return True
    else:
        return False


def distance(nano, pos):
    return sum([abs(nano[0][0] - pos[0]), abs(nano[0][1] - pos[1]), abs(nano[0][2] - pos[2])])


def distance_from_0(pos):
    return sum([abs(i) for i in pos])


def part_1():
    nanos = get_nanobots("2018_23_input.txt")
    print(nanos)
    max_radius_nano = max(nanos, key=lambda x: x[1])
    print(max_radius_nano)
    print('Part 1:', len([i for i in nanos if in_range(max_radius_nano, i)]))


part_1()


def brute_force():
    nanos = get_nanobots("2018_23_input.txt")
    min_x = min(nanos, key=lambda x: x[0][0])[0][0]
    max_x = max(nanos, key=lambda x: x[0][0])[0][0]
    min_y = min(nanos, key=lambda x: x[0][1])[0][1]
    max_y = max(nanos, key=lambda x: x[0][1])[0][1]
    min_z = min(nanos, key=lambda x: x[0][2])[0][2]
    max_z = max(nanos, key=lambda x: x[0][2])[0][2]
    max_number = 0
    max_pos = (0, 0, 0)
    # Brute force
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            for z in range(min_z, max_z):
                number = len([i for i in nanos if in_range_pos(i, (x, y, z))])
                if number >= max_number:
                    if number > max_number:
                        max_number = number
                        max_pos = (x, y, z)
                        print(max_pos)
                    elif distance_from_0((x, y, z)) < distance_from_0(max_pos):
                        max_number = number
                        max_pos = (x, y, z)
    return brute_force


def line_search(steps=100000):
    nanos = get_nanobots("2018_23_input.txt")
    min_x = min(nanos, key=lambda x: x[0][0])[0][0]
    max_x = max(nanos, key=lambda x: x[0][0])[0][0]
    min_y = min(nanos, key=lambda x: x[0][1])[0][1]
    max_y = max(nanos, key=lambda x: x[0][1])[0][1]
    min_z = min(nanos, key=lambda x: x[0][2])[0][2]
    max_z = max(nanos, key=lambda x: x[0][2])[0][2]
    max_number = 0
    max_pos = (0, 0, 0)
    for x in range(min_x, max_x, steps):
        for y in range(min_y, max_y, steps):
            for z in range(min_z, max_z, steps):
                number = len([i for i in nanos if in_range_pos(i, (x, y, z))])
                if number >= max_number:
                    if number > max_number:
                        max_number = number
                        max_pos = (x, y, z)
                        print(max_pos)
                    elif distance_from_0((x, y, z)) < distance_from_0(max_pos):
                        max_number = number
                        max_pos = (x, y, z)
                print(max_number, max_pos)
    return brute_force


def random_search(n, start=None, step=None):
    nanos = get_nanobots("2018_23_input.txt")
    min_x = min(nanos, key=lambda x: x[0][0])[0][0]
    max_x = max(nanos, key=lambda x: x[0][0])[0][0]
    min_y = min(nanos, key=lambda x: x[0][1])[0][1]
    max_y = max(nanos, key=lambda x: x[0][1])[0][1]
    min_z = min(nanos, key=lambda x: x[0][2])[0][2]
    max_z = max(nanos, key=lambda x: x[0][2])[0][2]
    if start is None:
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        z = random.randint(min_z, max_z)
    else:
        x = start[0]
        y = start[1]
        z = start[2]
    max_number = len([i for i in nanos if in_range_pos(i, (x, y, z))])
    max_pos = (x, y, z)
    for i in range(n):
        if step is not None:
            x += random.randint(-step, step)
            y += random.randint(-step, step)
            z += random.randint(-step, step)
        else:
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
            z = random.randint(min_z, max_z)
        number = len([i for i in nanos if in_range_pos(i, (x, y, z))])
        if number >= max_number:
            if number > max_number:
                max_number = number
                max_pos = (x, y, z)
            elif distance_from_0((x, y, z)) < distance_from_0(max_pos):
                max_number = number
                max_pos = (x, y, z)
        print(max_number, max_pos)


def make_plot(step,iterations, central=None, search_range=None, ):
    nanos = get_nanobots("2018_23_input.txt")
    if central is None:
        min_x = min(nanos, key=lambda x: x[0][0])[0][0]
        max_x = max(nanos, key=lambda x: x[0][0])[0][0]
        min_y = min(nanos, key=lambda x: x[0][1])[0][1]
        max_y = max(nanos, key=lambda x: x[0][1])[0][1]
        min_z = min(nanos, key=lambda x: x[0][2])[0][2]
        max_z = max(nanos, key=lambda x: x[0][2])[0][2]
    else:
        min_x = central[0]-search_range[0]
        max_x = central[0]+search_range[0]
        min_y = central[1]-search_range[1]
        max_y = central[1]+search_range[1]
        min_z = central[2]-search_range[2]
        max_z = central[2]+search_range[2]
    x_coords = []
    y_coords = []
    z_coords = []
    numbers = []
    max_number = 0
    max_pos = (0, 0, 0)
    for x in range(min_x, max_x, step):
        for y in range(min_y, max_y, step):
            for z in range(min_z, max_z, step):
                x_coords.append(x)
                y_coords.append(y)
                z_coords.append(z)
                number = len([i for i in nanos if in_range_pos(i, (x, y, z))])
                numbers.append(number)
                if number >= max_number:
                    if number > max_number:
                        max_number = number
                        max_pos = (x, y, z)
                    elif distance_from_0((x, y, z)) < distance_from_0(max_pos):
                        max_number = number
                        max_pos = (x, y, z)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x_coords, y_coords, z_coords, 'z', c=numbers)
    plt.show()
    print(max_number, max_pos)
    if iterations != 0 and int(step*2/3) != 0:
        return make_plot(int(step*2/3), iterations-1, central=max_pos, search_range=[int(i*2/3) for i in search_range])
    else:
        return [max_number, step, iterations, max_pos, search_range]


# line_search(10000000)
# random_search(100000, (54071424, 15640239, 45782556), 100000)
# make_plot(50000000)
# make_plot(10000000, (92725402, 1429081, 29478128), (50000000, 50000000, 50000000))
# make_plot(5000000, (62725402, 21429081, 39478128), (25000000, 25000000, 25000000))
# make_plot(2500000, (57725402, 16429081, 39478128), (12500000, 12500000, 12500000))
# make_plot(1250000, (56725402, 15929081, 44478128), (6250000, 6250000, 6250000))
# make_plot(612500, (51725402, 13429081, 44478128), (3750000, 3750000, 3750000))
# make_plot(612500, (52725402, 14429081, 44478128), (3750000, 3750000, 3750000))
# returned = make_plot(10000000, 25, (92725402, 1429081, 29478128), (50000000, 50000000, 50000000))
# print(returned)
# returned = make_plot(395, 25, (50372865, 12338002, 46178717), [1979, 1979, 1979])
# print(returned)
# [976, 1, 12, (50372507, 12337779, 46179014), [9, 9, 9]]
make_plot(10000000, 999, search_range=(50000000, 50000000, 50000000))
