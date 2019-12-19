from __future__ import print_function
import networkx as nx

rocky, wet, narrow = 0, 1, 2
torch, gear, neither = 0, 1, 2
valid_items = {rocky: (torch, gear), wet: (gear, neither), neither: (torch, neither)}
valid_regions = {torch: (rocky, narrow), gear: (rocky, wet), neither: (wet, narrow)}


def get_cave(file):
    with open(file) as f:
        lines = iter([line.strip() for line in f.read().strip().splitlines()])
        depth = int(next(lines)[len("depth: "):])
        target = tuple([int(n) for n in next(lines)[len("target: "):].split(",")])
    return depth, target


def generate_grid(depth, corner):
    # (x, y) -> geologic index, erosion level, risk
    grid = {}

    for y in range(0, corner[1] + 1):
        for x in range(0, corner[0] + 1):
            if (x, y) in [(0, 0), target]:
                geo = 0
            elif x == 0:
                geo = y * 48271
            elif y == 0:
                geo = x * 16807
            else:
                geo = grid[(x-1, y)][1] * grid[(x, y-1)][1]
            ero = (geo + depth) % 20183
            risk = ero % 3
            grid[(x, y)] = (geo, ero, risk)

    return grid


def dijkstra(grid, corner, target):
    graph = nx.Graph()
    for y in range(0, corner[1] + 1):
        for x in range(0, corner[0] + 1):
            items = valid_items[grid[(x, y)]]
            graph.add_edge((x, y, items[0]), (x, y, items[1]), weight=7)
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                new_x, new_y = x+dx, y+dy
                if 0 <= new_x <= corner[0] and 0 <= new_y <= corner[1]:
                    new_items = valid_items[grid[(new_x, new_y)]]
                    for item in set(items).intersection(set(new_items)):
                        graph.add_edge((x, y, item), (new_x, new_y, item), weight=1)

    return nx.dijkstra_path_length(graph, (0, 0, torch), (target[0], target[1], torch))


depth, target = get_cave("./2018_22_input.txt")
grid = generate_grid(depth, target)
print("Answer 1:", sum([v[2] for v in grid.values()]))

corner = (target[0] + 100, target[1] + 100)
grid = {c: v[2] for c, v in (generate_grid(depth, corner)).items()}
print("Answer 2:", dijkstra(grid, corner, target))


#########################################

import sys
import re
import heapq

with open('./2018_22_input.txt' if len(sys.argv) < 2 else sys.argv[1]) as f:
    data = list(f)

depth = int(re.findall('\d+', data[0])[0])
target = tuple(map(int, re.findall('\d+', data[1])))

print(depth)
print(target)

geologic = {}
for x in range(0, target[0]+300):
    for y in range(0, target[1]+300):
        if (x == 0):
            geologic[(x, y)] = y * 48271
        elif (y == 0):
            geologic[(x, y)] = x * 16807
        else:
            # wasted time on part 1 by not reading carefully: you multiply
            # *erosion* levels, not *geologic* indexes. The side effect is
            # that I needed to add depth in twice here:
            geologic[(x, y)] = (
                (geologic[(x-1, y)]+depth)*(geologic[(x, y-1)]+depth)) % 20183
geologic[(0, 0)] = 0
geologic[target] = 0

tot = 0
terrain = {}
for spot in geologic:
    erosion = (geologic[spot] + depth) % 20183
    terrain[spot] = erosion % 3
    if spot[0] <= target[0] and spot[1] <= target[1]:
        tot += terrain[spot]

print("Part 1:", tot)
# estimate, time-so-far, x, y, item
# item is 0, 1, or 2 - 0 means "neither", 1 means "light", 2 means "climbing gear"
# that numbering system means that the terrain/gear rules work out to
# "item X cannot be used in terrain X"
workheap = [(target[0] + target[1], 0, 0, 0, 1)]
besttime = {}
while workheap:
    (_, sofar, x, y, item) = heapq.heappop(workheap)
    # print(sofar)
    if (x, y) == target and item == 1:
        print("Part 2:", sofar)
        break
    neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    for n in neighbors:
        if n in terrain:
            if item != terrain[n]:
                if besttime.get((n[0], n[1], item), sofar + 999) > sofar + 1:
                    estimate = abs(n[0] - target[0]) + abs(n[1] - target[1])
                    if item != 1:
                        estimate += 7
                    heapq.heappush(
                        workheap, (estimate + sofar + 1, sofar + 1,
                                   n[0], n[1], item))
                    besttime[(n[0], n[1], item)] = sofar + 1
    for it in range(3):
        if it != terrain[(x, y)] and it != item:
            if besttime.get((x, y, it), sofar + 999) > sofar + 7:
                estimate = abs(x - target[0]) + abs(y - target[1])
                if it != 1:
                    estimate += 7
                heapq.heappush(
                    workheap, (estimate + sofar + 7, sofar + 7, x, y, it))
                besttime[(x, y, it)] = sofar + 7
