class Region:
    regions = {}

    def __init__(self, pos, depth, left, up, target):
        self.depth = depth
        self.pos = pos
        self.left = left
        self.up = up
        self.geo = get_geologic_index(self, target)
        self.risk = ((self.geo + self.depth) % 20183) % 3  # 0 : Rocky, 1 : Wet, 2 : Narrow


def get_geologic_index(region, target):
    if region.up is None and region.left is None:
        return 0
    elif region.pos == target:
        return 0
    elif region.up is None:
        return region.pos[1] * 16807
    elif region.left is None:
        return region.pos[0] * 48271
    else:
        return region.left.geo * region.up.geo


def get_geo(up, left, pos, target):
    if up is None and left is None:
        return 0
    elif pos == target:
        return 0
    elif up is None:
        return pos[1] * 16807
    elif left is None:
        return pos[0] * 48271
    else:
        return up*left


def get_erosion_level(region):
    return (region.geo + region.depth) % 20183


def get_type(erosion):
    return erosion % 3


def part_1_mod(depth, target):
    erosion_above = [None for x in range(target[0] + 1)]
    depth = depth
    depth_mod = depth % 20183
    y_max = target[1]
    x_max = target[0]
    sum_risk = 0
    for y in range(y_max + 1):
        erosion = None
        for x in range(x_max + 1):
            up = erosion_above[x]
            left = erosion
            if up is None and left is None:
                erosion = depth_mod
            elif [x, y] == target:
                erosion = depth_mod
            elif up is None:
                erosion = ((x * 16807) + depth) % 20183
            elif left is None:
                erosion = ((y * 48271) + depth) % 20183
            else:
                erosion = ((up * left) + depth) % 20183
            erosion_above[x] = erosion
            icon = {0: '.', 1: '=', 2: '|'}
            print(icon[erosion % 3], end='')
            sum_risk += erosion % 3
        print()
    print(sum_risk)


# part_1_mod(11739, [11, 718])


def part_2_map(depth, target, overshoot_x, overshoot_y):
    erosion_above = [None for x in range(target[0] + 1 + overshoot_x)]
    depth = depth
    depth_mod = depth % 20183
    y_max = target[1] + overshoot_y
    x_max = target[0] + overshoot_x
    cave_map = [[None for x in range(x_max + 1)] for y in range(y_max + 1)]
    sum_risk = 0
    for y in range(y_max + 1):
        erosion = None
        for x in range(x_max + 1):
            up = erosion_above[x]
            left = erosion
            if up is None and left is None:
                erosion = depth_mod
            elif [x, y] == target:
                erosion = depth_mod
            elif up is None:
                erosion = ((x * 16807) + depth) % 20183
            elif left is None:
                erosion = ((y * 48271) + depth) % 20183
            else:
                erosion = ((up * left) + depth) % 20183
            erosion_above[x] = erosion
            # icon = {0: '.', 1: '=', 2: '|'}
            risk = erosion % 3
            # print(icon[risk], end='')
            sum_risk += risk
            cave_map[y][x] = Tile([y, x], risk)
        # print()
    print(sum_risk)
    return cave_map


class Tile:
    def __init__(self, pos, type):
        self.pos = pos
        self.type = type  # 0 : Rocky, 1 : Wet, 2 : Narrow

    def distance(self, tile):
        return abs(tile.pos[0] - self.pos[0]) + abs(tile.pos[1] - self.pos[1])

    def adjacent(self, cave_map):
        adjacents = []
        if self.pos[0] > 0:
            adjacents.append(cave_map[self.pos[0]-1][self.pos[1]])
        if self.pos[0] < len(cave_map)-1:
            adjacents.append(cave_map[self.pos[0]+1][self.pos[1]])
        if self.pos[1] > 0:
            adjacents.append(cave_map[self.pos[0]][self.pos[1]-1])
        if self.pos[1] < len(cave_map[0])-1:
            adjacents.append(cave_map[self.pos[0]][self.pos[1]+1])
        return adjacents

    def valid_equipment(self):
        if self.type == 0:
            return [1, 2]
        elif self.type == 1:
            return [0, 2]
        else:
            return [0, 1]


def get_distance(pos_1, pos_2):
    return abs(pos_1[0] - pos_2[0]) + abs(pos_1[1] - pos_2[1])


def get_delta_g(square, test_square, equipped, target):
    if square == target:
        new_valid = [1]
        if test_square.type == 1:
            if equipped == 2:
                return 8, 1
            else:
                return 15, 1
    else:
        new_valid = square.valid_equipment()
    if equipped in new_valid:
        return 1, equipped
    else:
        old_valid = test_square.valid_equipment()
        for equipment in old_valid:
            if equipment in new_valid:
                return 8, equipment


def path_finding(end, start, cave_map):
    # Path-finding method
    # Used A* method : https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    # Add start to open list
    start.g = 0
    start.h = start.distance(end)
    start.f = start.g + start.h
    start.equipped = 1  # 0: Neither, 1: Torch, 2: Climbing gear
    open_list = [start]
    closed_list = []
    # Stop if open list is empty and target square not found
    while len(open_list) > 0:
        # Take lowest f cost square on open list
        # switch to closed list
        test_square = open_list.pop(0)
        # stop and return path when target square added to closed list
        if test_square == end:
            path = []
            while test_square != start:
                path.append(test_square)
                test_square = test_square.parent
            path.append(start)
            path.reverse()
            return path
        closed_list.append(test_square)
        # for each square on that square
        for square in test_square.adjacent(cave_map):
            # if not walkable or on closed list, ignore
            if square not in closed_list:
                delta_g, new_equipped = get_delta_g(square, test_square, test_square.equipped, end)
                # if it isn't on open list, add to open list
                if square not in open_list:
                    # Make current square its parent, record F, g, and h costs
                    open_list.append(square)
                    square.parent = test_square
                    square.g = square.parent.g + delta_g
                    square.equipped = new_equipped
                    square.h = square.distance(end)
                    square.f = square.g + square.h
                # if on open list
                else:
                    # check if lower g cost than current
                    if square.g > test_square.g + delta_g:
                        # if so, change parent to current, recalculate g and f
                        square.parent = test_square
                        square.g = square.parent.g + delta_g
                        square.equipped = new_equipped
                        square.f = square.g + square.h
                        # resort open list by f
                        # Maybe only need to do sorting here?? Currently out of loop
                open_list = sorted(open_list, key=lambda x: (x.f, x.pos[0], x.pos[1]))
    # return no path
    return None


def get_direction(end, start):
    if end.pos[0] > start.pos[0]:
        return 'Down'
    elif end.pos[0] < start.pos[0]:
        return 'Up'
    elif end.pos[1] > start.pos[1]:
        return 'Right'
    else:
        return 'Left'


# cave_map = part_2_map(510, [10, 10], 100, 100)
# path = path_finding(cave_map[10][10], cave_map[0][0], cave_map)
cave_map = part_2_map(11739, [11, 718], 50, 50)
path = path_finding(cave_map[718][11], cave_map[0][0], cave_map)
print(path[0].pos, path[0].equipped, path[0].g)
for i in range(1, len(path)):
    print(path[i].pos, path[i].equipped, path[i].g, path[i].equipped, end=' ')
    print(get_direction(path[i], path[i-1]))
print(path[-1].g)
