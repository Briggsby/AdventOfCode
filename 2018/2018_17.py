import numpy as np
import sys

def get_map(file):
    input_file = open(file, 'r').read().splitlines()
    # Go through each line
    coords = [[[int(j) for j in i[2:].split('..')] for i in sorted(line.split(', '))] for line in input_file]
    # Find min and max of x and max of y
    x_max = max([i[0] for i in coords])[0] + 5
    x_min = min([i[0] for i in coords])[0] - 5
    y_max = max([i[1] for i in coords])[0]
    # Make a map range from the min and max of any x value and the max y value
    clay_map = np.array([[0 for _ in range(x_max-x_min+1)] for _ in range(y_max+1)])
    clay_map[0, 500-x_min] = 2
    # Fill in map accordingly
    for loc in coords:
        clay_map[(loc[1][0]):(loc[1][-1]+1), (loc[0][0]-x_min):(loc[0][-1]+1-x_min)] = 1
    return clay_map, x_min


def print_map(clay_map):
    for y in clay_map:
        for x in y:
            print('.' if x == 0 else ('#' if x == 1 else ('+' if x == 2 else '~')), end='')
        print()


# def water_fall(source, clay_map, end_fall=False, print_maps=True):
#     if end_fall:
#         return clay_map, end_fall
#     while True:
#         if source[0]+1 > len(clay_map)-1:
#             end_fall = True
#             break
#         elif clay_map[source[0]+1, source[1]] == 2:
#             end_fall = True
#             break
#         elif clay_map[source[0]+1, source[1]] in (1, 3):
#             clay_map, end_fall = water_spread(source, clay_map, end_fall, print_maps)
#             end_fall = True
#             break
#         elif clay_map[source[0]+1, source[1]] == 0:
#             source[0] += 1
#             clay_map[source[0], source[1]] = 2
#             print(source, 'fall', end_fall)
#             if print_maps:
#                 print_map(clay_map)
#     return clay_map, end_fall
#
#
# def water_spread(source, clay_map, end_fall=False, print_maps=True):
#     if end_fall:
#         return clay_map, end_fall
#     directions = [-1, 1]
#     left_most = source[1]
#     right_most = source[1]+1
#     fall = []
#     result_end_fall = end_fall
#     original_source = [source[0], source[1]]
#     for direc in directions:
#         source = original_source
#         while True:
#             if source[1]+direc < 0 or source[1]+direc > len(clay_map[0])-1:
#                 break
#             elif clay_map[source[0]+1, source[1]] == 0:
#                 fall.append(source)
#                 break
#             elif clay_map[source[0], source[1]+direc] == 2:
#                 result_end_fall = True
#                 break
#             elif clay_map[source[0], source[1]+direc] in (1, 3):
#                 if direc == -1:
#                     left_most = source[1]
#                 else:
#                     right_most = source[1]+1
#                 break
#             else:
#                 source = [source[0], source[1]+direc]
#                 clay_map[source[0], source[1]] = 2
#                 print(source, 'spread', end_fall)
#                 if print_maps:
#                     print_map(clay_map)
#     if len(fall) > 0:
#         for i in fall:
#             clay_map, new_end_fall = water_fall(i, clay_map, end_fall, print_maps)
#             if new_end_fall:
#                 result_end_fall = True
#     else:
#         clay_map[source[0], left_most:right_most] = 3
#         clay_map, result_end_fall = water_spread([original_source[0]-1, original_source[1]],
#         clay_map, result_end_fall)
#     return clay_map, result_end_fall


def water_fall(source, clay_map, end_fall=False, print_maps=True):
    while True:
        # Fall until hit clay, water, or bottom of map
        if source[0]+1 >= len(clay_map):
            return clay_map
        next_square = clay_map[source[0]+1, source[1]]
        # If hitting clay or resting water, spread
        if next_square in (1, 3):
            return water_spread(source, clay_map)
        # If empty, fill with running water
        elif next_square == 0:
            source = [source[0]+1, source[1]]
            clay_map[source[0], source[1]] = 2
            # print_map(clay_map)
        # If running water, stop
        else:
            # print_map(clay_map)
            return clay_map


def water_spread(source, clay_map, end_fall=False, print_maps=True):
    # Spread water
    directions = [-1, 1]
    walls = 0
    left_side = source[1]
    right_side = source[1]
    original_source = [source[0], source[1]]
    # For both directions:
    for direction in directions:
        source = [original_source[0], original_source[1]]
        while True:
            # If out of map, stops
            if source[1]+direction < 0 or source[1]+direction >= len(clay_map[0]):
                break
            next_square = clay_map[source[0], source[1]+direction]
            below_square = clay_map[source[0]+1, source[1]]
            # If square below open, stop this direction and fall
            if below_square == 0:
                clay_map = water_fall(source, clay_map)
                break
            # If square below is running water,
            if below_square == 2:
                return clay_map
            # If hit clay or resting water, stop
            if next_square in (1, 3):
                if next_square == 1:
                    walls += 1
                break
            # If hits running water with a hole beneath it
            if next_square == 3 and clay_map[source[0]+1, source[1]+direction] in (0 or 2):
                break
            # Otherwise continue spreading
            else:
                source = [source[0], source[1]+direction]
                clay_map[source[0], source[1]] = 2
                if direction == -1:
                    left_side = source[1]
                else:
                    right_side = source[1]
                # print_map(clay_map)
                # print('**************')
    # If hit clay on both sides, make resting
    if walls == 2:
        if clay_map[original_source[0]-1, original_source[1]] == 0:
            # print_map(clay_map)
            clay_map[original_source[0]-1, original_source[1]] = 2
        clay_map[source[0], left_side:right_side+1] = 3
        # if left_side == right_side:
            # print_map(clay_map)
    return water_fall([original_source[0]-1, original_source[1]], clay_map)


test_map = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
clay_test = water_fall([0, 10], test_map)
print_map(clay_test)
tiles_reached = -1
tiles_left = 0
for y in clay_test:
    for x in y:
        if x in (2,3):
            tiles_reached += 1
        if x == 3:
            tiles_left += 1
print(tiles_reached, tiles_left)

sys.setrecursionlimit(1000000)
clay, x_min = get_map('2018_17_input.txt')
print(len(clay), len(clay[0]))
clay[0, 500-x_min] = 2
clay_2 = water_fall([0, 500-x_min], clay, print_maps=False)
print_map(clay_2)
tiles_reached = -1
tiles_left = 0
for y in clay_2:
    for x in y:
        if x in (2,3):
            tiles_reached += 1
        if x == 3:
            tiles_left += 1
print(tiles_reached, tiles_left)
