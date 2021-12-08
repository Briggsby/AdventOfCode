from collections import defaultdict

input_file = open("./2019/2019_3_input.txt", 'r').read().splitlines()
input_file = [line.strip().split(',') for line in input_file]

test0 = [['R8','U5','L5','D3'], ['U7','R6','D4','L4']]
test1 = [['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
         ['U62','R66','U55','R34','D71','R55','D58','R83']]
test2 = [['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
         ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']]

class Grid:
    def __init__(self, wire_paths):
        self.x_max_size = 0
        self.x_min_size = 0
        self.y_max_size = 0
        self.y_min_size = 0
        self.wires = 0
        self.locs = defaultdict(set)
        self.locs_length = defaultdict(lambda: defaultdict(lambda: None))
        self.crossings = set()
        for route in wire_paths:
            self.add_wire(route)

    def add_wire(self, route):
        loc = (0,0)
        self.wires += 1
        wire = self.wires

        wire_length = 0
        self.add_loc(loc, wire, wire_length)

        wire_length = 1
        for path in route:
            direction = path[0]
            distance = path[1]
            if direction == 'R':
                for i in range(loc[0]+1, loc[0]+distance+1):
                    self.add_loc((i, loc[1]), wire, wire_length)
                    wire_length += 1
                loc = (loc[0]+distance, loc[1])
            elif direction == 'L':
                for i in reversed(range(loc[0]-distance, loc[0])):
                    self.add_loc((i, loc[1]), wire, wire_length)
                    wire_length += 1
                loc = (loc[0]-distance, loc[1])
            elif direction == 'U':
                for i in reversed(range(loc[1]-distance, loc[1])):
                    self.add_loc((loc[0], i), wire, wire_length)
                    wire_length += 1
                loc = (loc[0], loc[1]-distance)
            elif direction == 'D':
                for i in range(loc[1]+1, loc[1]+distance+1):
                    self.add_loc((loc[0], i), wire, wire_length)
                    wire_length += 1
                loc = (loc[0], loc[1]+distance)

    def add_loc(self, loc, wire, wire_length):
        self.x_max_size = loc[0] if loc[0] > self.x_max_size else self.x_max_size
        self.x_min_size = loc[0] if loc[0] < self.x_min_size else self.x_min_size
        self.y_max_size = loc[1] if loc[1] > self.y_max_size else self.y_max_size
        self.y_min_size = loc[1] if loc[1] < self.y_min_size else self.y_min_size
        self.locs[loc].add(wire)
        if len(self.locs[loc]) > 1:
            self.crossings.add(loc)
        self.locs_length[loc][wire] = wire_length if self.locs_length[loc][wire] == None else self.locs_length[loc][wire]

    def print_board(self):
        for y in range(self.y_min_size, self.y_max_size+1):
            for x in range(self.x_min_size, self.x_max_size+1):
                symbol = '.' if len(self.locs[(x,y)]) == 0 else len(self.locs[(x,y)])
                print(symbol, end='')
            print('')

    def shortest_manhattan_crossing(self):
        crossing_distances = [sum([abs(i) for i in x]) for x in self.crossings]
        crossing_distances.remove(0)
        return min(crossing_distances)

    def shortest_length_crossing(self):
        crossing_distances = [sum([length for _, length in self.locs_length[x].items()]) for x in self.crossings]
        # crossing_distances = [[length for _, length in self.locs_length[x].items()] for x in self.crossings]
        print(crossing_distances)
        crossing_distances.remove(0)
        return min(crossing_distances)


test0_route = [[[y[0], int(y[1:])] for y in x] for x in test0]
test1_route = [[[y[0], int(y[1:])] for y in x] for x in test1]
test2_route = [[[y[0], int(y[1:])] for y in x] for x in test2]
input_route = [[[y[0], int(y[1:])] for y in x] for x in input_file]

print(test0_route)
test0_grid = Grid(test0_route)
print(test0_grid.shortest_manhattan_crossing())
print(test0_grid.shortest_length_crossing())

print(test1_route)
test1_grid = Grid(test1_route)
print(test1_grid.shortest_manhattan_crossing())
print(test1_grid.shortest_length_crossing())

print(test2_route)
test2_grid = Grid(test2_route)
print(test2_grid.shortest_manhattan_crossing())
print(test2_grid.shortest_length_crossing())

input_grid = Grid(input_route)
print(input_grid.shortest_manhattan_crossing())
print(input_grid.shortest_length_crossing())


