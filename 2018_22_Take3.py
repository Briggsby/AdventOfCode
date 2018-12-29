def get_erosion(coords, cave_map, depth, target):
    x = coords[0]
    y = coords[1]
    if coords in cave_map:
        return cave_map[coords]
    else:
        if x != 0 and y != 0:
            cave_map[coords] = get_erosion((x - 1, y), cave_map, depth, target)
            cave_map[coords] *= get_erosion((x, y - 1), cave_map, depth, target)
            cave_map[coords] = (cave_map[coords] + depth) % 20183
            return cave_map[coords]
        elif y == 0:
            cave_map[coords] = ((x * 16807) + depth) % 20183
            return cave_map[coords]
        elif x == 0:
            cave_map[coords] = ((y * 48271) + depth) % 20183
            return cave_map[coords]
        elif coords == target:
            cave_map[coords] = 0 + depth
            return cave_map[coords]


def get_risk(coords, cave_map, depth, target):
    return get_erosion(coords, cave_map, depth, target) % 3


def distance(coords_1, coords_2):
    distance = abs(coords_1[0] - coords_2[0]) + abs(coords_1[1] - coords_2[1])
    if coords_1[2] != coords_2[2]:
        distance += 7
    return distance


def available_levels(risk):
    return [i for i in range(3) if i != risk]


def get_adjacent(coords, cave_map, depth, target, check_out=True):
    x = coords[0]
    y = coords[1]
    z = coords[2]
    adjacent = []
    # Get up and down
    for i in available_levels(get_risk((x, y), cave_map, depth, target)):
        if z != i:
            adjacent.append((x, y, i))
    # Get adjacent
    for i in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if check_out or i in cave_map:
            if i[0] >= 0 and i[1] >= 0:
                if z in available_levels(get_risk((x, y), cave_map, depth, target)):
                    adjacent.append((i[0], i[1], z))
    return adjacent


def shortest_path(start, target, depth, cave_map=None):
    if cave_map is None:
        cave_map = dict()
    cave_map[(start[0], start[1])] = depth % 20183
    cave_map[(target[0], target[1])] = depth % 20183
    path_map = dict()

    open_list = [start]
    closed_list = []

    g = 0
    h = 1
    f = 2
    parent = 3

    path_map[start] = dict()
    path_map[start][g] = 0
    path_map[start][h] = distance(start, target)
    path_map[start][f] = g + h
    path_map[start][parent] = None

    while True:
        if len(open_list) < 1:
            return None
        current = open_list.pop(0)
        closed_list.append(current)
        if current == target:
            return path_map[current][g]
        adjacent = get_adjacent(current, cave_map, depth, target, False)
        for path in adjacent:
            if path not in closed_list:
                if path not in open_list:
                    open_list.append(path)
                    path_map[path] = dict()
                    path_map[path][parent] = current
                    path_map[path][g] = path_map[current][g] + distance(path, current)
                    path_map[path][h] = distance(path, target)
                    path_map[path][f] = path_map[path][g] + path_map[path][h]
                else:
                    if path_map[path][g] > path_map[current][g] + distance(path, current):
                        path_map[path][parent] = current
                        path_map[path][g] = path_map[current][g] + distance(path, current)
                        path_map[path][h] = distance(path, target)
                        path_map[path][f] = path_map[path][g] + path_map[path][h]
                open_list.sort(key=lambda x: path_map[x][f])


def make_map(depth, target, x_size, y_size):
    cave_map = dict()
    for x in range(x_size):
        cave_map[(x, 0)] = ((x * 16807) + depth) % 20183
    for y in range(1, y_size):
        cave_map[(0, y)] = ((y * 48271) + depth) % 20183
    for x in range(1, x_size):
        for y in range(1, y_size):
            cave_map[(x, y)] = ((cave_map[(x-1, y)] * cave_map[(x, y-1)]) + depth) % 20183
    return cave_map


cave_map_prepped = make_map(510, (10, 10), 311, 1000)
print(shortest_path((0, 0, 1), (10, 10, 1), 510, cave_map_prepped))
cave_map_prepped = make_map(11739, (11, 718), 311, 1000)
print(shortest_path((0, 0, 1), (11, 718, 1), 11739, cave_map_prepped))

