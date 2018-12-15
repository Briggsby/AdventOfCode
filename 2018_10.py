import re
import random

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


def get_average_squared_distance(points, samples = 1000):
    sum_dists = 0
    pos_sum = [0, 0]
    for i in range(samples):
        dists = 0
        sample = random.randint(0, len(points)-1)
        point = points[sample]
        for j in points:
            dists += abs(point[0][1] - j[0][1]) + abs(point[0][1] - j[0][1])
        dists /= len(points)
        sum_dists += dists
        pos_sum[0] += point[0][0]
        pos_sum[1] += point[0][1]
    return sum_dists/samples, [pos_sum[0]/samples, pos_sum[1]/samples]


def update_points(points, interval):
    for i in points:
        i[0][0] += i[1][0]*interval
        i[0][1] += i[1][1]*interval
    return points


def find_closest(points, time, intervals, start):
    points = update_points(points, start)
    for i in range(time):
        print('Time', start+(i*intervals))
        print(get_average_squared_distance(points))
        points = update_points(points, intervals)


#find_closest(points, 100000, 1, 10515)
# 10521 seconds is where they are closest, average position is 131.861, 108.715


def print_time(points, time, xmin, xmax, ymin, ymax):
    points = update_points(points, time)
    display = [['.'for i in range(xmax-xmin+1)] for i in range(ymax-ymin+1)]
    for i in points:
        display[i[0][1]-ymin][i[0][0]-xmin] = '#'
    for i in display:
        for j in i:
            print(j, end='')
        print()
    print()

print_time(points, 10521, 0, 200, 0, 200)
