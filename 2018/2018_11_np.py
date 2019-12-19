import numpy as np

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


def part_2(serial, grid_size):
        grid = np.matrix([[get_power_level(serial, x, y) for y in range(grid_size)] for x in range(grid_size)])
        for i in range(grid_size):
            print(i, max([np.sum(grid[x:(x+i),y:(y+i)]) for x in range(grid_size-i+1) for y in range(grid_size-i+1)]))

part_2(3463, 300)