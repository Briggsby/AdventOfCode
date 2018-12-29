import re

class Group:
    def __init__(self, units, hp, attack, type, initiative, weaknesses, immunities, team, id):
        self.units = units
        self.hp = hp
        self.attack_damage = attack
        self.attack_type = type
        self.initiative = initiative
        self.weaknesses = weaknesses[:]
        self.immunities = immunities[:]
        self.team = team
        self.dead = False
        self.id = id
        self.effective_attack = units * attack

    def __str__(self):
        return "Team " + str(self.team) + ", ID: " + str(self.id)

    def effective_power(self):
        return self.units * self.attack_damage

    def choose_target(self, targets):
        selected = [group for group in targets if self.attack_type in group.weaknesses]
        selected.sort(key=lambda x: (x.effective_power(), x.initiative), reverse=True)
        if len(selected) > 0:
            targets.remove(selected[0])
            return [selected[0], 2] # 2 for weak
        selected = [group for group in targets if self.attack_type not in group.immunities]
        selected.sort(key=lambda x: (x.effective_power(), x.initiative), reverse=True)
        if len(selected) > 0:
            targets.remove(selected[0])
            return [selected[0], 1] # 1 for normal
        return [None, None]

    def choose_target_2(self, targets):
        selected = [group for group in targets if self.attack_type in group.weaknesses and not group.dead]
        selected.sort(key=lambda x: (x.effective_power(), x.initiative), reverse=True)
        if len(selected) > 0:
            targets.remove(selected[0])
            return [selected[0], 2]  # 2 for weak
        selected = [group for group in targets if self.attack_type not in group.immunities and not group.dead]
        selected.sort(key=lambda x: (x.effective_power(), x.initiative), reverse=True)
        if len(selected) > 0:
            targets.remove(selected[0])
            return [selected[0], 1]  # 1 for normal
        # selected = [group for group in targets if self.attack_type in group.immunities and not group.dead]
        # selected.sort(key=lambda x: (x.effective_power(), x.initiative), reverse=True)
        # if len(selected) > 0:
        #    targets.remove(selected[0])
        #    return [selected[0], 0] # 0 for immune
        return [None, None]

    def take_damage(self, amount, mult):
        damage = amount * mult
        units_lost = min(int(damage/self.hp), self.units)
        if units_lost <= 0:
            print(self, 'lost no units, staying at', self.units)
            return 0
        print(self, "lost", units_lost, "units, going from", self.units, "to", self.units - units_lost)
        self.units -= units_lost
        self.effective_attack = self.units * self.attack_damage
        if self.units <= 0:
            self.dead = True
        return units_lost

    def boost(self, boost, team_cond=0):
        if self.team == team_cond:
            self.attack_damage += boost
        return self


def find_targets(groups, groups_0, groups_1):
    targets = {}
    groups_0 = groups_0[:]
    groups_1 = groups_1[:]
    for i in groups:
        targets[i] = i.choose_target(groups_1 if i.team == 0 else groups_0)
        print(i, "would attack", targets[i][0], 'for', i.effective_power() * targets[i][1], 'damage')
    return targets


def find_targets_2(groups, groups_0, groups_1):
    targets = {}
    groups_0 = groups_0[:]
    groups_1 = groups_1[:]
    for i in groups:
        if not i.dead:
            target = i.choose_target_2(groups_1 if i.team == 0 else groups_0)
            if target[0] is not None:
                targets[i] = target
                print(i, "would attack", targets[i][0], 'for', i.effective_power() * targets[i][1], 'damage')
    return targets


def attacking_phase(groups, targets):
    casualties = []
    for i in groups:
        if not i.dead:
            if targets[i][0] is not None:
                if not targets[i][0].dead:
                    targets[i][0].take_damage(i.effective_power(), targets[i][1])
                    if targets[i][0].dead:
                        casualties.append(targets[i][0])
    return casualties


def attacking_phase_2(groups, targets):
    stalemate = True
    for i in groups:
        if not i.dead:
            if i in targets:
                if not targets[i][0].dead:
                    print(i, "attacks", targets[i][0])
                    lost_units = targets[i][0].take_damage(i.effective_power(), targets[i][1])
                    if stalemate:
                        if lost_units > 0:
                            stalemate = False
    return stalemate


def battle(groups):
    groups_target_choosing = sorted(groups, key=lambda x: (x.effective_power(), x.initiative), reverse=True)
    groups_initiative = sorted(groups, key=lambda x: x.initiative, reverse=True)
    groups_0 = [group for group in groups if group.team == 0]
    groups_1 = [group for group in groups if group.team == 1]
    while True:
        targets = find_targets(groups_target_choosing, groups_0, groups_1)
        casualties = attacking_phase(groups_initiative, targets)
        for i in casualties:
            groups_target_choosing.remove(i)
            groups_initiative.remove(i)
            groups_0.remove(i)
            groups_1.remove(i)
        if len(groups_0) == 0 or len(groups_1) == 1:
            if len(groups_0) == 0:
                return sum([group.units for group in groups_1])
            else:
                return sum([group.units for group in groups_0])


def battle_report(groups_0, groups_1):
    print('Team 0')
    for i in groups_0:
        if not i.dead:
            print('Group', i.id, 'contains', i.units, 'units')
    print('Team 1')
    for i in groups_1:
        if not i.dead:
            print('Group', i.id, 'contains', i.units, 'units')


def battle_2(groups):
    groups = groups[:]
    groups_initiative = sorted(groups, key=lambda x: x.initiative, reverse=True)
    groups_0 = [group for group in groups if group.team == 0]
    groups_1 = [group for group in groups if group.team == 1]
    while True:
        battle_report(groups_0, groups_1)
        groups_target_choosing = sorted(groups, key=lambda x: (x.effective_power(), x.initiative), reverse=True)
        targets = find_targets_2(groups_target_choosing, groups_0, groups_1)
        if len(targets) == 0:
            alive_0 = [group for group in groups if group.team == 0 and not group.dead]
            alive_1 = [group for group in groups if group.team == 1 and not group.dead]
            if len(alive_0) > 0 and len(alive_1) > 0:
                print('Stalemate reached')
                return None
            else:
                break
        stalemate = attacking_phase_2(groups_initiative, targets)
        if stalemate:
            print('Stalemate reached')
            return None
    units_left = [group for group in groups if not group.dead]
    return units_left[0].team, sum([group.units for group in units_left])


def test_groups():
    groups = [Group(17,   5390, 4507, 'fire', 2, ['radiation', 'bludgeoning'], [], 0, 1),
              Group(989,  1274, 25, 'slashing', 3, ['bludgeoning', 'slashing'], ['fire'], 0, 2),
              Group(801,  4706, 116, 'bludgeoning', 1, ['radiation'], [], 1, 1),
              Group(4485, 2961, 12, 'slashing', 4, ['fire', 'cold'], ['radiation'], 1, 2)]
    return groups


def input_groups():
    groups = [
              Group(3916,  3260,  8,   'radiation',   16, [], [],                                   0, 0),
              Group(4737,  2664,  5,   'slashing',    13, [], ['radiation', 'cold', 'bludgeoning'], 0, 1),
              Group(272,   10137, 331, 'slashing',    10, [], [],                                   0, 2),
              Group(92,    2085,  223, 'bludgeoning', 1,  [], ['fire'],                             0, 3),
              Group(126,   11001, 717, 'bludgeoning', 8,  ['cold', 'fire'], ['bludgeoning'],        0, 4),
              Group(378,   4669,  117, 'fire',        17, [], ['cold', 'slashing'],                 0, 5),
              Group(4408,  11172, 21,  'bludgeoning', 5,  ['bludgeoning'], ['slashing'],            0, 6),
              Group(905,   11617, 100, 'fire',        20, ['fire'], [],                             0, 7),
              Group(3574,  12385, 27,  'radiation',   19, ['bludgeoning'], ['radiation'],           0, 8),
              Group(8186,  3139,  3,   'bludgeoning', 9,  [], ['bludgeoning', 'fire'],              0, 9),
              Group(273,   26361, 172, 'radiation',   18, ['slashing'], ['radiation'],                   1, 0),
              Group(536,   44206, 130, 'bludgeoning', 12, ['fire', 'cold'], [],                          1, 1),
              Group(1005,  12555, 24,  'radiation',   6,  [], ['fire', 'radiation', 'bludgeoning'],      1, 2),
              Group(2381,  29521, 23,  'slashing',    4,  [], ['bludgeoning', 'radiation'],              1, 3),
              Group(5162,  54111, 19,  'fire',        2,  ['radiation'], [],                             1, 4),
              Group(469,   45035, 163, 'radiation',   15, ['fire', 'slashing'], [],                      1, 5),
              Group(281,   23265, 135, 'radiation',   11, ['slashing'], ['bludgeoning'],                 1, 6),
              Group(4350,  46138, 18,  'bludgeoning', 14, ['fire'], [],                                  1, 7),
              Group(3139,  48062, 28,  'bludgeoning', 3,  ['cold'], ['bludgeoning', 'slashing', 'fire'], 1, 8),
              Group(9326,  41181, 8,   'cold',        7,  ['fire', 'bludgeoning'], [],                   1, 9),
    ]
    return groups


def read_input(file):
    raw = open(file).read()
    teams = raw.split("\n\n")
    teams = [i.splitlines()[1:] for i in teams]
    regex = re.compile("(\d+) units each with (\d+) hit points with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)")
    regex_immune = re.compile("(\d+) units each with (\d+) hit points \(immune to ([a-z, ]+)\) with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)")
    regex_weak = re.compile("(\d+) units each with (\d+) hit points \(weak to ([a-z, ]+)\) with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)")
    regex_immuneweak = re.compile("(\d+) units each with (\d+) hit points \(immune to ([a-z, ]+); weak to ([a-z, ]+)\) with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)")
    regex_weakimmune = re.compile("(\d+) units each with (\d+) hit points \(weak to ([a-z, ]+); immune to ([a-z, ]+)\) with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)")
    groups = []
    for team in range(len(teams)):
        current_id = 0
        for group in teams[team]:
            if 'immune' in group and 'weak' in group:
                if group.find('immune') < group.find('weak'):
                    group_info = regex_immuneweak.match(group).groups()
                    groups.append(
                        Group(int(group_info[0]), int(group_info[1]), int(group_info[4]), group_info[5],
                              int(group_info[6]),
                              group_info[3].split(', '), group_info[2].split(', '), team, current_id))
                else:
                    group_info = regex_weakimmune.match(group).groups()
                    groups.append(
                        Group(int(group_info[0]), int(group_info[1]), int(group_info[4]), group_info[5],
                              int(group_info[6]),
                              group_info[2].split(', '), group_info[3].split(', '), team, current_id))
            elif 'immune' in group:
                group_info = regex_immune.match(group).groups()
                groups.append(
                    Group(int(group_info[0]), int(group_info[1]), int(group_info[3]), group_info[4], int(group_info[5]),
                          [], group_info[2].split(', '), team, current_id))
            elif 'weak' in group:
                group_info = regex_weak.match(group).groups()
                groups.append(
                    Group(int(group_info[0]), int(group_info[1]), int(group_info[3]), group_info[4], int(group_info[5]),
                          group_info[2].split(', '), [], team, current_id))
            else:
                group_info = regex.match(group).groups()
                groups.append(
                    Group(int(group_info[0]), int(group_info[1]), int(group_info[2]), group_info[3], int(group_info[4]),
                          [], [], team, current_id))
            current_id += 1
    return groups

# print(battle_2(test_groups()))
# print(battle_2(input_groups()))

# print(battle_2(read_input("2018_24_test.txt")))
print(battle_2(read_input("2018_24_input.txt")))


def boosted_battle(file, boost):
    boosted_groups = [group.boost(boost) for group in read_input(file)]
    return battle_2(boosted_groups)


def part_2(file, lower=0, upper=10000):
    if boosted_battle(file, upper)[0] != 0:
        return 'Upper bound too low'
    else:
        middle = int((upper+lower))/2
        while True:
            if lower > upper:
                print('Best Found')
                return boosted_battle(file, upper), upper
            middle = int((upper+lower)/2)
            results = boosted_battle(file, middle)
            if results is None:
                while True:
                    middle += 1
                    results = boosted_battle(file, middle)
                    if results is not None:
                        break
                lower = middle + 1
            elif results[0] != 0:
                lower = middle+1
            else:
                upper = middle-1


print(boosted_battle("2018_24_test.txt", 1570))
# print(part_2("2018_24_input.txt"))
print(boosted_battle('2018_24_input.txt', 131))

