input_file = open('2018_6_input.txt', 'r').read().splitlines()


# Method 1
# This uses a lot of sorts at the beginning, but none are nested
def quick_coords(coords):
    coords = coords.split(', ')
    return [int(coords[0]), int(coords[1])]


coordinates = [quick_coords(x) for x in input_file]
indices = range(0, len(coordinates))
cities = dict(zip([tuple(x) for x in coordinates], indices))
x_coordinates = [x[0] for x in coordinates]
y_coordinates = [x[1] for x in coordinates]
x_sorted_indices = sorted(indices, key=lambda x: coordinates[x][0])
y_sorted_indices = sorted(indices, key=lambda x: coordinates[x][1])
sorted_indices = [[x_sorted_indices.index(x), y_sorted_indices.index(x)] for x in indices]
max_x = max(x_coordinates)
max_y = max(y_coordinates)
min_x = min(x_coordinates)
min_y = min(y_coordinates)
print('x_sorted_indices:', x_sorted_indices)
print('y_sorted_indices:', y_sorted_indices)
print('Sorted Indices:', sorted_indices)
print('Cities:', cities)


def get_closest_city(coords, first_check=False):
    closest_cities = []
    found_distance = 0
    for distance in range(1, max_x + max_y + 1):
        found_city = False
        test_coords = get_coords_distance(coords, distance)
        for i in test_coords:
            test_coord = tuple(i)
            if test_coord in cities:
                closest_cities.append(cities[tuple(test_coord)])
                found_city = True
        if found_city:
            found_distance = distance
            break
    if first_check:
        return closest_cities
    if len(closest_cities) > 1:
        return [-1, found_distance]  # This means multiple cities
    else:
        return [closest_cities[0], found_distance]


def get_coords_distance(coords, distance):
    poss_additions = [[0, 0]]*((distance+1)*4-4)
    # Add the 4 corner pieces
    poss_additions[0] = [coords[0], coords[1]-distance]
    poss_additions[1] = [coords[0]+distance, coords[1]]
    poss_additions[2] = [coords[0], coords[1]+distance]
    poss_additions[3] = [coords[0]-distance, coords[1]]
    # Then add all the ones in between
    index = 4
    for i in range(1, distance):
        poss_additions[index] = [poss_additions[0][0]+i, poss_additions[0][1]+i]
        poss_additions[index+1] = [poss_additions[1][0]-i, poss_additions[1][1]+i]
        poss_additions[index+2] = [poss_additions[2][0]-i, poss_additions[2][1]-i]
        poss_additions[index+3] = [poss_additions[3][0]+i, poss_additions[3][1]-i]
        index += 4
    return poss_additions


def get_closest_y_coord(coords, x_sorted_indices, y_sorted_indices):
    for i in x_sorted_indices:
        x_distance = coordinates[i][0]
        y_distance = coordinates[i][1]


# Get extremes

def get_extremes():
    extremes = []

    for x in range(min_x-1, max_x+2):
        for y in [min_y-1, max_y+1]:
            extremes.append([x, y, get_closest_city([x, y])])
    for x in [min_x-1, max_x+1]:
        for y in range(min_y, max_y+1):
            extremes.append([x, y, get_closest_city([x, y])])
    extreme_uniques = set([x[2][0] for x in extremes])
    print('Min X / Max X:', min_x, max_x, 'Min Y / Max Y:', min_y, max_y)
    print('Extremes:', extremes)
    print('Unique Extremes:', extreme_uniques)
    return extremes, extreme_uniques


def do_part_1():
    extremes, extreme_uniques = get_extremes()
    areas = {}
    for i in cities:
        if cities[i] not in extreme_uniques:
            areas[cities[i]] = -1
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            city = get_closest_city([x, y])
            if city[0] not in extreme_uniques:
                areas[city[0]] += 1
    print('Areas:', areas)
    biggest_area = 0
    biggest_area_city = 0
    for c in areas:
        if areas[c] > biggest_area:
            biggest_area = areas[c]
            biggest_area_city = c

    print(biggest_area, biggest_area_city)


# Part 2


def get_distance(coord1, coord2):
    return abs(coord2[0]-coord1[0])+abs(coord2[1]-coord1[1])


def do_part_2():
    region = 0
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            distance_sum = 0
            for i in coordinates:
                distance = get_distance([x, y], i)
                distance_sum += distance
                if distance_sum >= 10000:
                    break
            if distance_sum < 10000:
                region += 1
    return region


def do_part_2_method_2():
    region = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            distances = [get_distance([x, y], i) for i in coordinates]
            if sum(distances) < 10000:
                region += 1
    return region


import time
start = time.time()
print(do_part_2())
end = time.time()
print('method 1 took', end-start, 'seconds')
start = time.time()
print(do_part_2_method_2())
end = time.time()
print('method 2 took', end-start, 'seconds')
