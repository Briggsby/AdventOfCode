import re

input_file = open('2018_10_input.txt', 'r').read().splitlines()


def get_points(input_line):
    input_line = re.split('[<,>]', input_line)
    return [[int(input_line[1]), int(input_line[2])], [int(input_line[4]), int(input_line[5])]]


points = [get_points(i) for i in input_file]


def print_points(points):
    min_x = points[0][0][0]
    max_x = points[0][0][0]
    min_y = points[0][0][1]
    max_y = points[0][0][1]
    for i in points:
        if i[0][0] < min_x:
            min_x = i[0][0]
        if i[0][0] > max_x:
            max_x = i[0][0]
        if i[0][1] < min_y:
            min_y = i[0][1]
        if i[0][1] > max_y:
            max_y = i[0][1]
    display = [['.'for i in range(max_x-min_x+1)] for i in range(max_y-min_y+1)]
    for i in points:
        display[i[0][1]-min_y][i[0][0]-min_x] = '#'
    for i in display:
        for j in i:
            print(j, end='')
        print()
    print()


def update_points(points, interval):
    for i in points:
        i[0][0] += i[1][0]*interval
        i[0][1] += i[1][1]*interval
    return points


def part_1(points, time, intervals, start):
    points = update_points(points, start)
    for i in range(time):
        print('Time', i)
        print_points(points)
        points = update_points(points, intervals)


part_1(points, 5, 1, 10000)