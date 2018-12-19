def get_map(file):
    text = open(file, 'r').read().splitlines()
    max_width = max([len(line) for line in text])
    max_height = len(text)
    mine_map = [['' for _ in range(max_width)] for _ in range(max_height)]
    carts = []
    for y in range(max_height):
        for x in range(max_width):
            mine_map[y][x], cart = get_icon(text[y][x], [y, x])
            if cart is not None:
                carts.append(cart)
    return mine_map, carts


def get_icon(character, pos):
    cart = None
    icon = None
    if character == '<':
        cart = Cart(pos, [0, -1], str(pos[0])+str(pos[1]))
    elif character == '^':
        cart = Cart(pos, [-1, 0], str(pos[0])+str(pos[1]))
    elif character == '>':
        cart = Cart(pos, [0, 1], str(pos[0])+str(pos[1]))
    elif character == 'v':
        cart = Cart(pos, [1, 0], str(pos[0])+str(pos[1]))
    elif character is '/' or character is '+' or character is '\\':
        icon = character
    return icon, cart


def print_map(mine_map, cart_map=None):
    for y in range(len(mine_map)):
        for x in range(len(mine_map[0])):
            if cart_map is not None:
                if cart_map[y][x] is not None:
                    print(cart_map[y][x].cart_icon(), end='')
                else:
                    print(mine_map[y][x] or ' ', end='')
            else:
                print(mine_map[y][x] or ' ', end='')
        print()


class CartManager:
    def __init__(self, mine_map, carts, time=0):
        self.map = mine_map
        self.carts = sorted(carts, key=lambda item: (item.pos[0], item.pos[1]))
        self.cart_map = self.make_cart_map()
        self.time = time
        self.crashes = []

    def update(self):
        self.time += 1
        crashes = []
        cart_list = list(self.carts)
        for cart in cart_list:
            if not cart.crashed:
                crash = self.update_cart(cart)
                if crash is not None:
                    crashes.append(crash)
        self.carts = sorted(self.carts, key=lambda item: (item.pos[0], item.pos[1]))
        return crashes

    def make_cart_map(self):
        cart_map = [[None for _ in range(len(self.map[0]))] for _ in range(len(self.map))]
        for cart in self.carts:
            cart_map[cart.pos[0]][cart.pos[1]] = cart
        return cart_map

    def update_cart(self, cart):
        self.cart_map[cart.pos[0]][cart.pos[1]] = None
        cart.move()
        if self.cart_map[cart.pos[0]][cart.pos[1]] is not None:
            crash = ['Crash', self.time, cart.pos, cart.id, self.cart_map[cart.pos[0]][cart.pos[1]].id]
            cart.crashed = True
            self.cart_map[cart.pos[0]][cart.pos[1]].crashed = True
            self.carts.remove(cart)
            self.carts.remove(self.cart_map[cart.pos[0]][cart.pos[1]])
            self.cart_map[cart.pos[0]][cart.pos[1]] = None
            return crash
        else:
            self.cart_map[cart.pos[0]][cart.pos[1]] = cart
            if self.map[cart.pos[0]][cart.pos[1]] is not None:
                cart.turn(self.map[cart.pos[0]][cart.pos[1]])
            return None


class Cart:
    def __init__(self, pos, direction, cart_id):
        self.pos = pos
        self.dir = direction
        self.id = cart_id
        self.turn_state = 0
        self.crashed = False

    def move(self):
        self.pos = [self.pos[0]+self.dir[0], self.pos[1]+self.dir[1]]

    def cart_icon(self):
        if self.dir == [0, 1]:
            return '>'
        elif self.dir == [1, 0]:
            return 'v'
        elif self.dir == [-1, 0]:
            return '^'
        else:
            return '<'

    def turn(self, icon):
        if icon == '/':
            self.dir = [-self.dir[1], -self.dir[0]]
        elif icon == '\\':
            self.dir = [self.dir[1], self.dir[0]]
        elif icon == '+':
            if self.turn_state == 0:
                self.dir = [-self.dir[1], self.dir[0]]
            elif self.turn_state == 2:
                self.dir = [self.dir[1], -self.dir[0]]
            self.turn_state = (self.turn_state + 1) % 3


def part_1(file):
    mine_map, carts = get_map(file)
    cart_manager = CartManager(mine_map, carts)
    print('Beginning:')
    print_map(cart_manager.map, cart_manager.cart_map)
    crashes = []
    while len(crashes) == 0:
        new_crashes = cart_manager.update()
        crashes += new_crashes
        # print('Tick: ', cart_manager.time)
        # print_map(cart_manager.map, cart_manager.cart_map)
    print(cart_manager.time, crashes)


def part_2(file):
    mine_map, carts = get_map(file)
    cart_manager = CartManager(mine_map, carts)
    print('Beginning:')
    print_map(cart_manager.map, cart_manager.cart_map)
    crashes = []
    while len(cart_manager.carts) > 1:
        new_crashes = cart_manager.update()
        crashes += new_crashes
        # print('Tick: ', cart_manager.time)
        # print_map(cart_manager.map, cart_manager.cart_map)
    print_map(cart_manager.map, cart_manager.cart_map)
    print(cart_manager.time, crashes)
    print(cart_manager.carts[0].pos)


test = '2018_13_test.txt'
problem_input = '2018_13_input.txt'
test_2 = '2018_13_test_2.txt'

part_1(problem_input)
part_2(problem_input)
