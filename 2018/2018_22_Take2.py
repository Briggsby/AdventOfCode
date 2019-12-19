def get_map(depth, x_max, y_max, target):
    # Get erosions
    cave_map = dict()
    cave_map[(0, 0)] = depth % 20183
    for x in range(1, x_max):
        cave_map[(x, 0)] = ((x * 16807) + depth) % 20183
    for y in range(1, y_max):
        cave_map[(0, y)] = ((y * 48271) + depth) % 20183
    for x in range(1, x_max):
        for y in range(1, y_max):
            cave_map[(x, y)] = cave_map[(x-1, y)] * cave_map[(x, y-1)]
            cave_map[(x, y)] = (cave_map[(x, y)] + depth) % 20183
    cave_map[target] = depth % 20183
    return cave_map


def get_erosion(coords, cave_map, depth, target):
    x = coords[0]
    y = coords[1]
    if coords in cave_map:
        return cave_map[coords]
    else:
        if y == 0:
            cave_map[coords] = ((x * 16807) + depth) % 20183
            return cave_map[coords]
        elif x == 0:
            cave_map[coords] = ((y * 48271) + depth) % 20183
            return cave_map[coords]
        elif coords == target:
            cave_map[coords] = 0 + depth
            return cave_map[coords]
        else:
            cave_map[coords] = get_erosion((x-1, y), cave_map, depth, target)
            cave_map[coords] *= get_erosion((x, y-1), cave_map, depth, target)
            cave_map[coords] = (cave_map[coords] + depth) % 20183
            return cave_map[coords]


def sum_rectangle(x_max, y_max, depth, target, cave_map=None):
    if cave_map is None:
        cave_map = dict()
    return cave_map, sum([get_erosion((x, y), cave_map, depth, target) % 3 for x in range(x_max) for y in range(y_max)])


def print_map(cave_map, x_max, y_max):
    icon = {0: '.', 1: '=', 2: '|'}
    for y in range(y_max):
        for x in range(x_max):
            print(icon[cave_map[(x, y)] % 3], end='')
        print()


def shortest_path(start, depth, target, cave_map=None):
    if cave_map is None:
        cave_map = dict()
    open_list = [start]
    closed_list = []
    results = dict()

    g = 0
    h = 1
    f = 2
    equipment = 3
    parent = 4

    results[start] = dict()
    results[start][g] = 0
    results[start][h] = abs(target[0]-start[0]) + abs(target[1]-start[1])
    results[start][f] = results[start][g] + results[start][h]
    results[start][equipment] = 1
    results[start][parent] = None

    while True:
        if len(open_list) < 1:
            return None
        current = open_list.pop(0)
        current_type = get_erosion(current, cave_map, depth, target) % 3
        closed_list.append(current)
        if current == target:
            return results[target][g]
        x = current[0]
        y = current[1]
        adjacent = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        for i in adjacent:
            if i not in closed_list and i[0] >= 0 and i[1] >= 0:
                zone_type = get_erosion(i, cave_map, depth, target) % 3
                delta, equip = get_delta(i, target, zone_type, current_type, results[current][equipment])
                if i not in open_list:
                    open_list.append(i)
                    results[i] = dict()
                    results[i][g] = results[current][g] + delta
                    results[i][equipment] = equip
                    results[i][h] = abs(target[0]-i[0]) + abs(target[1]-i[1])
                    if equip != 1:
                        results[i][h] += 7
                    results[i][f] = results[i][g] + results[i][h]
                    results[i][parent] = current
                    # open_list.sort(key=lambda x: results[x][f])
                else:
                    if results[current][g] + delta < results[i][g]:
                        results[i][g] = results[current][g] + delta
                        results[i][equipment] = equip
                        results[i][f] = results[i][g] + results[i][h]
                        results[i][parent] = current
                        open_list.sort(key=lambda x: results[x][f])


def get_delta(dest, target, dest_type, current_type, equip):
    if dest == target:
        if equip == 1:
            return 1, equip
        else:
            if current_type == 1:
                if equip == 0:
                    return 15, 1
                else: # equip == 2
                    return 8, 1
            else:
                return 8, 1
    else:
        if dest_type != equip:
            return 1, equip
        else:
            if equip == 0:
                if current_type == 1:
                    return 8, 2
                else:
                    return 8, 1
            elif equip == 1:
                if current_type == 0:
                    return 8, 2
                else:
                    return 8, 0
            else:
                if current_type == 0:
                    return 8, 1
                else:
                    return 8, 0


cave, summed = sum_rectangle(11, 11, 510, (10, 10))
print_map(cave, 11, 11)
print(summed)

print(shortest_path((0, 0), 11739, (11, 718)))


# cave, summed = sum_rectangle(12, 719, 11739, (11, 718))
# print(shortest_path((0, 0), 11739, (11, 718)))
