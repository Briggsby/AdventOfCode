import time


class Room:
    rooms = {}

    def __init__(self):
        self.pos = None
        self.up = None
        self.down = None
        self.right = None
        self.left = None
        self.start_distance = None

    def __repr__(self):
        return 'Room with pos ' + str(self.pos[0]) + ', ' + str(self.pos[1])

    def set_pos(self, pos):
        Room.rooms[(pos[0], pos[1])] = self
        self.pos = [pos[0], pos[1]]

    def map(self, direction):
        new_room = None
        if direction == 'W':
            if (self.pos[0], self.pos[1]-1) in Room.rooms:
                new_room = Room.rooms[(self.pos[0], self.pos[1]-1)]
                self.left = new_room
                self.left.right = self
            else:
                new_room = Room()
                self.left = new_room
                self.left.right = self
                self.left.set_pos([self.pos[0], self.pos[1]-1])
        elif direction == 'E':
            if (self.pos[0], self.pos[1]+1) in Room.rooms:
                new_room = Room.rooms[(self.pos[0], self.pos[1]+1)]
                self.right = new_room
                self.right.left = self
            else:
                new_room = Room()
                self.right = new_room
                self.right.left = self
                self.right.set_pos([self.pos[0], self.pos[1]+1])
        elif direction == 'N':
            if (self.pos[0]-1, self.pos[1]) in Room.rooms:
                new_room = Room.rooms[(self.pos[0]-1, self.pos[1])]
                self.up = new_room
                self.up.down = self
            else:
                new_room = Room()
                self.up = new_room
                self.up.down = self
                self.up.set_pos([self.pos[0]-1, self.pos[1]])
        elif direction == 'S':
            if (self.pos[0]+1, self.pos[1]) in Room.rooms:
                new_room = Room.rooms[(self.pos[0]+1, self.pos[1])]
                self.down = new_room
                self.down.up = self
            else:
                new_room = Room()
                self.down = new_room
                self.down.up = self
                self.down.set_pos([self.pos[0]+1, self.pos[1]])
        new_room.distance_from_start()
        return new_room

    def distance_from_start(self):
        self.start_distance = min([adj.start_distance for adj in self.adjacent() if adj.start_distance is not None]) + 1
        return self.start_distance

    def distance(self, end):
        return abs(self.pos[0] - end.pos[0]) + abs(self.pos[1] - end.pos[1])

    def adjacent(self):
        adjacents = [self.up, self.left, self.right, self.down]
        return [adj for adj in adjacents if adj is not None]


def map_doors(current_locations, directions, i, coord_limits):
    original_current_locations = [room for room in current_locations]
    other_locations = []
    coord_limits = coord_limits[:]
    # Coord limits are : 0 - min_y, 1- max_y, 2 - min_x, 3 - max_x
    while True:
        if directions[i] == '$' or directions[i] == ')':
            all_locations = list(set(current_locations+other_locations))
            return all_locations, i+1, coord_limits
        elif directions[i] == '(':
            current_locations, i, coord_limits = map_doors(current_locations, directions, i+1, coord_limits)
        elif directions[i] == '|':
            other_locations = [room for room in current_locations]
            current_locations = [room for room in original_current_locations]
            i = i+1
        elif directions[i] in ('E', 'S', 'W', 'N'):
            for r in range(len(current_locations)):
                new_location = current_locations[r].map(directions[i])
                if new_location in current_locations:
                    current_locations[r] = None
                else:
                    current_locations[r] = new_location
                    if current_locations[r].pos[0] < coord_limits[0]:
                        coord_limits[0] = current_locations[r].pos[0]
                    elif current_locations[r].pos[0] > coord_limits[1]:
                        coord_limits[1] = current_locations[r].pos[0]
                    if current_locations[r].pos[1] < coord_limits[2]:
                        coord_limits[2] = current_locations[r].pos[1]
                    elif current_locations[r].pos[1] > coord_limits[3]:
                        coord_limits[3] = current_locations[r].pos[1]
            current_locations = [loc for loc in current_locations if loc is not None]
            i = i+1


def print_rooms():
    min_y = min(y[0] for y in Room.rooms)
    max_y = max(y[0] for y in Room.rooms)
    min_x = min(x[1] for x in Room.rooms)
    max_x = max(x[1] for x in Room.rooms)
    rooms = [[Room.rooms[(y, x)] if (y, x) in Room.rooms else None for x in range(min_x, max_x+1)] for y in range(min_y, max_y+1)]
    for y in range(len(rooms)):
        for x in range(len(rooms[0])):
            if rooms[y][x] is not None:
                print('X' if rooms[y][x].pos == [0, 0] else '.', end='')
                print('#' if rooms[y][x].right is None else '|', end='')
            else:
                print('#', end='')
                print('#', end='')
        print()
        for x in range(len(rooms[0])):
            if rooms[y][x] is not None:
                print('#' if rooms[y][x].down is None else '-', end='')
                print('#', end='')
            else:
                print('#', end='')
                print('#', end='')
        print()


def shortest_path(start, end):
    # Path-finding method
    # Used A* method : https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
    # Add start to open list
    start.g = 0
    start.h = start.distance(end)
    start.f = start.g + start.h
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
        for square in test_square.adjacent():
            # if it isn't on open list, add to open list
            if square not in closed_list:
                if square not in open_list:
                    # Make current square its parent, record F, g, and h costs
                    open_list.append(square)
                    square.parent = test_square
                    square.g = square.parent.g + 1
                    square.h = square.distance(end)
                    square.f = square.g + square.h
                # if on open list
                else:
                    # check if lower g cost than current
                    if square.g > test_square.g + 1:
                        # if so, change parent to current, recalculate g and f
                        square.parent = test_square
                        square.g = square.parent.g + 1
                        square.f = square.g + square.h
                        # resort open list by f
                        # Maybe only need to do this here?? Currently out of loop
                open_list = sorted(open_list, key=lambda x: (x.f, x.pos[0], x.pos[1]))
    # return no path
    return None


def find_longest_shortest_path():
    longest_path_length = 0
    longest_path = None
    for room_1 in Room.rooms:
        for room_2 in Room.rooms:
            if room_1 is not room_2:
                path = shortest_path(Room.rooms[room_1], Room.rooms[room_2])
                if len(path) > longest_path_length:
                    longest_path_length = len(path)
                    longest_path = path
    print(longest_path)
    print(longest_path_length-1)


def get_longest_shortest_path():
    longest = None
    distance = 0
    for room in Room.rooms:
        if Room.rooms[room].start_distance > distance:
            distance = Room.rooms[room].start_distance
            longest = Room.rooms[room]
    return distance, longest


def get_paths_over(n):
    paths = []
    for room in Room.rooms:
        if Room.rooms[room].start_distance >= n:
            paths.append(Room.rooms[room])
    return len(paths), paths


input_file = open('2018_20_input.txt', 'r').read()
test_1 = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'
test_2_23 = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
test_3_31 = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'
test_weird_14_not9 = '^WWWW(SSSSS|)WWWWW$'
test_slow_maybe_93 = '^(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)(N|S|E|W)$'
first_room = Room()
first_room.set_pos([0, 0])
first_room.start_distance = 0
print(map_doors([first_room], input_file[1:], i=0, coord_limits=[0, 0, 0, 0]))
print(Room.rooms)
print_rooms()
print(get_longest_shortest_path())
print(get_paths_over(1000))

start = time.time()
map_doors([first_room], input_file[1:], i=0, coord_limits=[0, 0, 0, 0])
print(time.time() - start)
start = time.time()
map_doors([first_room], test_slow_maybe_93[1:], i=0, coord_limits=[0, 0, 0, 0])
print(time.time() - start)

# After solving puzzle found out from the subreddit that the
# real puzzle doesn't actually need branching paths,
# because branches always come back to the original room
# in the example input and tests
# My solution works for branching paths since I was making it
# general, but, although recursive
# methods aren't even strictly necessary for that case,
# they are definitely overkill for non-branching paths
