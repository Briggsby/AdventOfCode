class Pot:
    def __init__(self, val, plant=False, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.plant = plant
        self.next = False
        if left is not None:
            left.right = self
        if right is not None:
            right.left = self

    def update(self):
        if self.next:
            self.make_plant()
        else:
            self.plant = False
        self.next = False

    def make_plant(self):
        self.plant = True
        if self.left is None:
            self.left = Pot(self.val-1, False, None, self)
        if self.left.left is None:
            self.left.left = Pot(self.val-2, False, None, self.left)
        if self.right is None:
            self.right = Pot(self.val+1, False, self, None)
        if self.right.right is None:
            self.right.right = Pot(self.val+2, False, self.right, None)

    def get_most_left(self):
        if self.left is None:
            return self
        else:
            return self.left.get_most_left()

    def get_most_right(self):
        if self.right is None:
            return self
        else:
            return self.right.get_most_left()

    def pos(self, index):
        if index == 0:
            return self
        elif index > 0:
            return self.get_right(index)
        else:
            return self.get_left(-index)

    def get_left(self, index):
        if index == 1:
            return self.left
        elif self.left is None:
            return None
        else:
            return self.left.get_left(index-1)

    def get_right(self, index):
        if index == 1:
            return self.right
        elif self.right is None:
            return None
        else:
            return self.right.get_right(index-1)

    def two_left(self):
        return self.left.left

    def two_right(self):
        return self.right.right


def read_plants(file):
    input_file = open(file, 'r').read().splitlines()
    initial_state = input_file[0][15:]
    rules = input_file[2:]
    return initial_state, rules


def read_rules(raw_rules, state_length=5, separate=True):
    rules = []
    for raw in raw_rules:
        state = [True if i == '#' else False for i in raw[:state_length]]
        centre = state[int(state_length/2)]
        result = True if raw[len(raw)-1] == '#' else False
        rules.append([centre, state, result])
    if separate:
        plant_rules = [[rule[1], rule[2]] for rule in rules if rule[0]]
        pot_rules = [[rule[1], rule[2]] for rule in rules if not rule[0]]
        return plant_rules, pot_rules
    return rules


def set_up(initial_state):
    print('Setting up:', initial_state)
    starting_pot = Pot(0, True if initial_state[0] == '#' else False)
    previous_pot = starting_pot
    for i in range(1, len(initial_state)):
        val = i
        previous_pot = Pot(val, True if initial_state[i] == '#' else False, previous_pot)
    extra_pot_right_1 = Pot(previous_pot.val+1, False, previous_pot)
    extra_pot_right_2 = Pot(previous_pot.val+2, False, extra_pot_right_1)
    extra_pot_left_1 = Pot(starting_pot.val-1, False, None, starting_pot)
    extra_pot_left_2 = Pot(starting_pot.val-2, False, None, extra_pot_left_1)
    return starting_pot


def update(pot, plant_rules, pot_rules, rule_result_index=1):
    starting_pot = pot.get_most_left()
    pot = starting_pot
    while True:
        if pot.plant:
            for rule in plant_rules:
                if check_rule(rule, pot):
                    # print('Rule:', pot.val, rule[0], rule[1])
                    pot.next = rule[rule_result_index]
                    break
        else:
            for rule in pot_rules:
                if check_rule(rule, pot):
                    pot.next = rule[rule_result_index]
        if pot.right is None:
            break
        else:
            pot = pot.right
    pot = starting_pot
    while True:
        pot.update()
        if pot.right is None:
            break
        else:
            pot = pot.right
    return starting_pot.get_most_left()


def check_rule(rule, pot, rule_state_index=0):
    for i in range(len(rule[rule_state_index])):
        index = i-int((len(rule[rule_state_index])/2))
        pot_check = pot.pos(index)
        plant_check = False
        if pot_check is not None:
            plant_check = pot_check.plant
        if plant_check is not rule[rule_state_index][i]:
            return False
    return True


def sum_plant_numbers(pot):
    starting_pot = pot.get_most_left()
    pot = starting_pot
    summed = 0
    while True:
        if pot.plant:
            summed += pot.val
        if pot.right is not None:
            pot = pot.right
        else:
            break
    return summed


def print_pots(pot):
    starting_pot = pot.get_most_left()
    pot = starting_pot
    while True:
        if pot.plant:
            print('#', end='')
        else:
            print('.', end='')
        if pot.right is not None:
            pot = pot.right
        else:
            break
    print()


def part_1(pot_input, generations):
    initial_state, raw_rules = read_plants(pot_input)
    starting_pot = set_up(initial_state)
    plant_rules, pot_rules = read_rules(raw_rules)
    print_pots(starting_pot)
    print(sum_plant_numbers(starting_pot))
    for i in range(generations):
        update(starting_pot, plant_rules, pot_rules)
        # print_pots(starting_pot)
        print(i+1, sum_plant_numbers(starting_pot))
    return sum_plant_numbers(starting_pot)


test = '2018_12_test.txt'
problem_input = '2018_12_input.txt'

print(part_1(test, 20))
print(part_1(problem_input, 20))
# print(part_1(problem_input, 500))
# Becomes stable to increasing by 65 each generation
# At 200 is 13956
print((50000000000-200)*65+13956)


