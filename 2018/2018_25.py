def manhattan_distance(coords_1, coords_2):
    summed = 0
    for i in range(len(coords_1)):
        summed += abs(coords_1[i] - coords_2[i])
    return summed


def get_constellations(coordinates):
    constellations = dict()
    new_constellation_index = 0
    for coord_1 in coordinates:
        matched_constellations = []
        for constellation in constellations:
            for coord_2 in constellations[constellation]:
                if manhattan_distance(coord_1, coord_2) <= 3:
                    matched_constellations.append(constellation)
                    break
        if len(matched_constellations) == 0:
            constellations[new_constellation_index] = [coord_1]
            new_constellation_index += 1
        elif len(matched_constellations) == 1:
            constellations[matched_constellations[0]].append(coord_1)
        else:
            new_constellation = [constellations[c] for c in matched_constellations]
            new_constellation = [item for c in new_constellation for item in c]
            constellations[new_constellation_index] = new_constellation
            constellations[new_constellation_index].append(coord_1)
            new_constellation_index += 1
            for i in matched_constellations:
                constellations.pop(i)
    return len(constellations), constellations


def get_coordinates(file):
    return [[int(i) for i in line.split(',')] for line in open(file).read().splitlines()]


# print(get_constellations(get_coordinates("2018_25_test_2.txt")))
# print(get_constellations(get_coordinates("2018_25_test_4.txt")))
# print(get_constellations(get_coordinates("2018_25_test_3.txt")))
# print(get_constellations(get_coordinates("2018_25_test_8.txt")))
print(get_constellations(get_coordinates("2018_25_input.txt")))
