import re

input_file = open('2018_4_input.txt', 'r').read().splitlines()
print(input_file)
input_file = [re.split('[\[\]\-: ]', line) for line in input_file]
print(input_file)

all_info = [[line[1:6], line[7:]] for line in input_file]
print(all_info)
all_info = [["".join(line[0]), line[1]] for line in all_info]
print(all_info)
all_sorted = sorted(all_info, key=lambda x: x[0])
print(all_sorted)
guard_sleeps = {}
biggest_sleeper = 0
biggest_sleep = 0
active_guard = 0
sleep = None
sleep_time = 0
for i in all_sorted:
    if len(i[1]) > 2:  # If it is a guard announcement
        if active_guard not in guard_sleeps:
            guard_sleeps[active_guard] = sleep_time
        else:
            guard_sleeps[active_guard] += sleep_time
        if guard_sleeps[active_guard] > biggest_sleep:
            biggest_sleep = guard_sleeps[active_guard]
            biggest_sleeper = active_guard
        sleep_time = 0
        new_guard_id = int(i[1][1][1:])
        active_guard = new_guard_id
        if sleep:
            print('Warning, guard found asleep at end of shift')
    else:
        if sleep is None:
            sleep = int(i[0][10:])
        else:
            sleep_time += int(i[0][10:]) - sleep
            sleep = None
print(biggest_sleeper, 'was the biggest sleeper, slept', biggest_sleep, 'minutes')


# Now we have the biggest sleeper, time to work out when he slept most
guard_biggest_sleeper = False
sleep = None
sleep_times = [0]*60
for i in all_sorted:
    if len(i[1]) > 2:
        if guard_biggest_sleeper:
            guard_biggest_sleeper = False
        if int(i[1][1][1:]) == biggest_sleeper:
            guard_biggest_sleeper = True
    else:
        if guard_biggest_sleeper:
            if sleep is None:
                sleep = int(i[0][10:])
            else:
                sleep_start = sleep
                sleep_finish = int(i[0][10:])
                for minute in range(sleep_start, sleep_finish):
                    sleep_times[minute] += 1
                sleep = None

print(sleep_times)
max_sleep_counter = max(sleep_times)
max_sleep_time = 0
for i in range(len(sleep_times)):
    if sleep_times[i] == max_sleep_counter:
        max_sleep_time = i

print('Guard ', biggest_sleeper, 'slept most on minute', max_sleep_time, 'on', max_sleep_counter, 'occasions')
print('Answer is', biggest_sleeper, '*', max_sleep_time, '=', biggest_sleeper*max_sleep_time)


# Part 2
# Pretty much the same, except we store every single guard's entire schedule
print('Starting Part 2')
guard_sleeps = {}
active_guard = 0
sleep = None
base_sleep_times = [0]*60
biggest_sleep_occasions = 0
biggest_sleep_minute = 0
biggest_sleep_minute_guard = 0
for i in all_sorted:
    if len(i[1]) > 2:  # If it is a guard announcement
        new_guard_id = int(i[1][1][1:])
        active_guard = new_guard_id
        if sleep:
            print('Warning, guard found asleep at end of shift')
            sleep = None
    else:
        if sleep is None:
            sleep = int(i[0][10:])
        else:
            sleep_start = sleep
            sleep_finish = int(i[0][10:])
            if active_guard not in guard_sleeps:
                guard_sleeps[active_guard] = base_sleep_times[:]
            for minute in range(sleep_start, sleep_finish):
                guard_sleeps[active_guard][minute] += 1
            sleep = None
            biggest_guard_sleep_occasions = max(guard_sleeps[active_guard])
            if biggest_guard_sleep_occasions > biggest_sleep_occasions:
                biggest_sleep_occasions = biggest_guard_sleep_occasions
                for minute in range(sleep_start, sleep_finish):
                    if guard_sleeps[active_guard][minute] == biggest_sleep_occasions:
                        biggest_sleep_minute = minute
                        biggest_sleep_minute_guard = active_guard

print('Biggest sleeper on any given minute was', biggest_sleep_minute_guard, 'who slept on minute',
      biggest_sleep_minute, biggest_sleep_occasions, 'times')

print('Answer to part 2:', biggest_sleep_minute_guard, '*', biggest_sleep_minute, '=',
      biggest_sleep_minute*biggest_sleep_minute_guard)


# Wanted to make it print a schedule like in the challenge
graph = []
active_guard = 0
active_date_index = -1
sleep = None
for entry in all_sorted:
    if len(entry[1]) > 2:  # If it is a guard announcement
        active_date_index += 1
        new_date = entry[0][:8]
        new_guard_id = int(entry[1][1][1:])
        active_guard = new_guard_id
        graph.append([new_date, new_guard_id, ['.']*60])
    else:
        if sleep is None:
            sleep = int(entry[0][10:])
        else:
            sleep_start = sleep
            sleep_finish = int(entry[0][10:])
            for minute in range(sleep_start, sleep_finish):
                graph[active_date_index][2][minute] = '#'
            sleep = None


print('Date', end=' '*6)
print('ID', end=' '*4)
print('Minute')
print(' '*16, end='')
for i in range(5):
    for j in range(10):
        print(i, end='')
print()
print(' '*16, end='')
for i in range(5):
    for j in range(10):
        print(j, end='')
print()
for entry in graph:
    print(entry[0], end=' '*2)
    print(entry[1],end=' '*(6-len(str(entry[1]))))
    for i in entry[2]:
        print(i, end='')
    print()






