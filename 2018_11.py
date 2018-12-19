def get_power_level(serial, x, y):
    rack_ID = x + 10
    power = rack_ID*y
    power += serial
    power *= rack_ID
    str_power = str(power)
    if len(str_power) < 3:
        return -5
    else:
        return int(str_power[len(str_power)-3]) - 5


def part_1(grid_size, serial, grid=None, square_size=3, square_grid=None, square_grid_size=2, do_print=False):
    if grid is None:
        grid = [[None for y in range(grid_size)] for x in range(grid_size)]
    if square_grid is None:
        square_grid = [[None for y in range(grid_size)] for x in range(grid_size)]
    highest_power_sum = 0
    highest_power_loc = []
    for x in range(grid_size-square_size+1):
        for y in range(grid_size-square_size+1):
            power_sum = 0
            if square_grid[x][y] is None:
                for x_delt in range(square_size):
                    for y_delt in range(square_size):
                        x_test = x+x_delt
                        y_test = y+y_delt
                        if grid[x_test][y_test] is None:
                            grid[x_test][y_test] = get_power_level(serial, x_test+1, y_test+1)
                        power_sum += grid[x_test][y_test]
            else:
                power_sum += square_grid[x][y]
                for x_delt in range(square_grid_size, square_size):
                    for y_delt in range(square_size):
                        x_test = x+x_delt
                        y_test = y+y_delt
                        if grid[x_test][y_test] is None:
                            grid[x_test][y_test] = get_power_level(serial, x_test+1, y_test+1)
                        power_sum += grid[x_test][y_test]
                for y_delt in range(square_grid_size, square_size):
                    for x_delt in range(square_size):
                        x_test = x + x_delt
                        y_test = y + y_delt
                        if grid[x_test][y_test] is None:
                            grid[x_test][y_test] = get_power_level(serial, x_test + 1, y_test + 1)
                        power_sum += grid[x_test][y_test]
            square_grid[x][y] = power_sum
            if power_sum > highest_power_sum:
                highest_power_sum = power_sum
                highest_power_loc = [x, y]
    if do_print:
        for x in range(grid_size):
            for y in range(grid_size):
                power = grid[x][y]
                if power is None:
                    print("", end="")
                else:
                    if power < 0:
                        print(power, end='  ')
                    else:
                        print(' ', power, sep='', end='  ')
            print()
        print()
    return highest_power_sum, highest_power_loc, square_size, square_grid, grid


print(get_power_level(57, 122, 79))
print(get_power_level(39, 217, 196))
print(get_power_level(71, 101, 153))


print(part_1(300, 18)[0:3])
print(part_1(300, 42)[0:3])
print(part_1(300, 3463)[0:3])


def part_2(serial, grid_size, print_each = False):
    highest_power = 0
    highest_power_loc = []
    highest_power_grid_size = 0
    grid = [[get_power_level(serial, x, y) for y in range(grid_size)] for x in range(grid_size)]
    square_grid = [[get_power_level(serial, x, y) for y in range(grid_size)] for x in range(grid_size)]
    for i in range(2, grid_size+1):
        highest_power_ind = -999999
        highest_power_loc_ind = []
        for x in range(grid_size-i+1):
            for y in range(grid_size-i+1):
                added_power = 0
                for y_add in range(0, i):
                    added_power += grid[x+i-1][y+y_add]
                for x_add in range(0, i-1):
                    added_power += grid[x+x_add][y+i-1]
                square_grid[x][y] += added_power
                if square_grid[x][y] > highest_power:
                    highest_power = square_grid[x][y]
                    highest_power_loc = [x+1, y+1]
                    highest_power_grid_size = i
                if square_grid[x][y] > highest_power_ind:
                    highest_power_ind = square_grid[x][y]
                    highest_power_loc_ind = [x, y]
        print(highest_power_ind, highest_power_loc_ind, i)
    print(highest_power, highest_power_loc, highest_power_grid_size)


print(part_2(3463, 300, True))
