class CombatManager:
    # Combat manager class
    def __init__(self, input_map, no_losses=False, elf_attack=3):
        # Stores map of squares and units
        self.elf_attack = elf_attack
        self.map = []
        self.map, self.unit_map, self.units = self.read_input(input_map)
        self.elves = [unit for unit in self.units if unit.elf]
        self.gobs = [unit for unit in self.units if not unit.elf]
        self.round = 0
        self.combat = False
        self.dead_units = []
        self.no_losses = no_losses

    def read_input(self, input_map):
        # Read input and make map of square and units
        input_file = open(input_map, 'r').read().splitlines()
        max_width = max([len(line) for line in input_file])
        max_height = len(input_file)
        square_map = [[Square([y, x], self) for x in range(max_width)] for y in range(max_height)]
        unit_map = [[None for _ in range(max_width)] for _ in range(max_height)]
        units = []
        for y in range(max_height):
            for x in range(max_width):
                if input_file[y][x] == '#':
                    square_map[y][x].wall = True
                elif input_file[y][x] != '.':
                    unit = Unit(input_file[y][x] == 'E', self, [y, x], attack=self.elf_attack if input_file[y][x] == 'E' else 3)
                    units.append(unit)
                    unit_map[y][x] = unit
        return square_map, unit_map, units

    def print_map(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.unit_map[y][x] is not None:
                    print('E' if self.unit_map[y][x].elf else 'G', end='')
                else:
                    print('#' if self.map[y][x].wall else '.', end='')
            print()

    def start_combat(self):
        self.combat = True
        # While combat isn't ended, repeat rounds
        while True:
            print('Round', self.round+1)
            # Each round, assigns initiative
            initiative = sorted(self.units, key=lambda x: (x.pos[0], x.pos[1]))
            # Then makes each unit take its turn
            for unit in initiative:
                if not unit.dead:
                    unit.turn()
                if not self.combat:
                    break
            if not self.combat:
                break
            # Increase round counter by 1
            self.round += 1
            self.print_map()

    def end_combat(self):
        # When combat ends, print sum of hit points
        # and number of full rounds
        self.combat = False
        sum_hp = sum([unit.hp for unit in self.units])
        print('End of Combat')
        self.print_map()
        print('Elves' if self.units[0].elf else 'Gobbos', 'won!')
        print('In', self.round, 'rounds with', sum_hp, 'left on', len(self.units), 'units')
        print(sum_hp*self.round)

    def end_combat_early(self, elf_id):
        # End combat because of an elf dying
        self.combat = False
        print('End of combat, elf', elf_id, 'has fallen in round', self.round)
        print(len(self.gobs), 'gobs remain')


class Square:
    def __init__(self, pos, manager):
        # position
        self.pos = pos
        # map
        self.manager = manager
        # Wall or not
        self.wall = False

    # methods for above, left, right, down
    def above(self):
        if self.pos[0] != 0:
            return self.manager.map[self.pos[0]-1][self.pos[1]]
        else:
            return None

    def left(self):
        if self.pos[1] != 0:
            return self.manager.map[self.pos[0]][self.pos[1]-1]
        else:
            return None

    def right(self):
        if self.pos[1] != len(self.manager.map[0])-1:
            return self.manager.map[self.pos[0]][self.pos[1] + 1]
        else:
            return None

    def down(self):
        if self.pos[0] != len(self.manager.map)-1:
            return self.manager.map[self.pos[0]+1][self.pos[1]]
        else:
            return None

    def adjacent(self):
        return [i for i in [self.above(), self.left(), self.right(), self.down()] if i is not None]

    def distance(self, square):
        return abs(self.pos[0] - square.pos[0]) + abs(self.pos[1] - square.pos[1])

    def unit(self):
        return self.manager.unit_map[self.pos[0]][self.pos[1]]


class Unit:
    # Unit class
    def __init__(self, elf, manager, pos, hp=200, attack=3):
        self.dead = False
        # Elf or goblin (bool)
        self.elf = elf
        # Position
        self.pos = pos
        self.manager = manager
        self.hp = hp
        self.attack_score = attack
        self.id = str(pos[0])+str(pos[1])

    def square(self):
        return self.manager.map[self.pos[0]][self.pos[1]]

    def turn(self):
        # Turn order:
        # Ties are always broken top to bottom, left to right
        # if in range of target, attack immediately:
        if self.try_attack():
            return
        # End combat if no targets (no round finishes)
        if len(self.targets()) == 0:
            self.manager.end_combat()
            return

        # Identify each possible target
        target_squares = []
        for target in self.targets():
            # Identify each open square adjacent to each target
            for square in target.square().adjacent():
                if not square.wall and square.unit() is None:
                    target_squares.append(square)
        # Decide which square could be reached in the fewest steps
        if len(target_squares) == 0:
            return
        target_squares = sorted(target_squares, key=lambda x: (x.pos[0], x.pos[1]))
        shortest_path = None
        shortest_dest = None
        for square in target_squares:
            new_path = self.path_finding(square)
            if new_path is not None:
                if shortest_path is None:
                    shortest_path = new_path
                    shortest_dest = square
                elif len(new_path) < len(shortest_path):
                    shortest_path = new_path
                    shortest_dest = square
        # Move a single step towards that square by shortest path
        if shortest_path is not None:
            for square in self.square().adjacent():
                if square.unit() is None and not square.wall:
                    if square is shortest_path[0]:
                        self.move(square)
                        break
                    else:
                        path = self.path_finding(shortest_dest, square)
                        if path is not None:
                            if len(path) <= len(shortest_path):
                                self.move(square)
                                break
            self.try_attack()
        # End turn

    def targets(self):
        return self.manager.gobs if self.elf else self.manager.elves

    def try_attack(self):
        target = None
        for square in self.square().adjacent():
            if square.unit() is not None:
                if square.unit().elf != self.elf:
                    if target is None:
                        target = square.unit()
                    elif square.unit().hp < target.hp:
                        target = square.unit()
        if target is not None:
            self.attack(target)
            return True
        else:
            return False

    def attack(self, target):
        # Attack method
        # print('Elf' if self.elf else 'Gob', self.id, 'attacks', 'Elf' if target.elf else 'Gob', target.id)
        # Reduce target's hp by attack power
        target.hp -= self.attack_score
        # If 0, target dies
        if target.hp <= 0:
            print('Elf' if self.elf else 'Gob', self.id, 'killed', 'Elf' if target.elf else 'Gob', target.id, '!')
            target.die()

    def die(self):
        self.manager.unit_map[self.pos[0]][self.pos[1]] = None
        self.manager.units.remove(self)
        if self.elf:
            self.manager.elves.remove(self)
            if self.manager.no_losses:
                self.manager.end_combat_early(self.id)
        else:
            self.manager.gobs.remove(self)
        self.dead = True

    def path_finding(self, end, start=None):
        # Path-finding method
        # Used A* method : https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
        # Add start to open list
        if start is None:
            start = self.square()
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
                path.reverse()
                return path
            closed_list.append(test_square)
            # for each square on that square
            for square in test_square.adjacent():
                # if not walkable or on closed list, ignore
                if not square.wall and square.unit() is None and square not in closed_list:
                    # if it isn't on open list, add to open list
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

    def move(self, location):
        # remove self from map location
        self.manager.unit_map[self.pos[0]][self.pos[1]] = None
        # put self in new map location
        self.manager.unit_map[location.pos[0]][location.pos[1]] = self
        # change pos
        self.pos = location.pos


def part_1():
    comb_manager = CombatManager('2018_15_input.txt')
    comb_manager.print_map()
    comb_manager.start_combat()


def part_2():
    comb_manager = CombatManager('2018_15_input.txt', no_losses=True, elf_attack=12)
    comb_manager.start_combat()


part_2()
