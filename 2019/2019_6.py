class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None
        self.children = {}

    def update_parent(self, parent):
        self.parent = parent
        parent.children[self] = 1
        parent.propagate(self.children)

    def propagate(self, new_children):
        new_children = {key: value+1 for key,value in new_children.items()}
        self.children.update(new_children)
        if self.parent is not None:
            self.parent.propagate(self.children)

full_map = {}

def convert_to_orbit(orbit):
    orbit = orbit.split(')')
    parent = orbit[0]
    child = orbit[1]
    if parent not in full_map:
        full_map[parent] = Node(parent)
    if child not in full_map:
        full_map[child] = Node(child)
        full_map[child].update_parent(full_map[parent])
    else:
        full_map[child].update_parent(full_map[parent])

test = ['COM)B',
'B)C',
'C)D',
'D)E',
'E)F',
'B)G',
'G)H',
'D)I',
'E)J',
'J)K', 'K)L']

for i in test:
    convert_to_orbit(i)

orbits = 0
for i, k in full_map.items():
    orbits += len(k.children.items())

print(orbits)

input_file = open("2019/2019_6_input.txt", 'r').read().splitlines()
full_map = {}
for i in input_file:
    convert_to_orbit(i)

orbits = 0
for i, k in full_map.items():
    orbits += len(k.children.items())

print(orbits)
you_orbit = full_map['YOU'].parent
print(you_orbit.name)
santa_orbit = full_map['SAN'].parent
print(santa_orbit.name)


closest_planet = None
closest_distance = 99999
for i, k in full_map.items():
    if you_orbit in k.children and santa_orbit in k.children:
        distance = k.children[you_orbit] + k.children[santa_orbit]
        if distance < closest_distance:
            closest_planet = k
            closest_distance = distance

print(closest_distance)
print(closest_planet.name) 