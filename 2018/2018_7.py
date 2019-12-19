input_file = open('2018_7_input.txt', 'r').read().splitlines()


def get_step_prereqs(instructions, step_index=5, prereq_index=36):
    step = instructions[prereq_index]
    prerequisite = instructions[step_index]
    return step, prerequisite


def make_step_list(input_instructions):
    step_prereqs = {}
    done_steps = {}
    for line in input_instructions:
        step, prereq = get_step_prereqs(line)
        if step in step_prereqs:
            step_prereqs[step].append(prereq)
        else:
            step_prereqs[step] = [prereq]
        if step not in done_steps:
            done_steps[step] = False
        if prereq not in done_steps:
            done_steps[prereq] = False
    return step_prereqs, done_steps


def try_do_step(step, step_prereqs, done_steps, order):
    if step in step_prereqs:
        prereqs = sorted([x for x in step_prereqs[step] if not done_steps[x]])
        if len(prereqs) < 1:
            return do_step(step, done_steps, order)
        else:
            return try_do_step(prereqs[0], step_prereqs, done_steps, order)
    else:
        return do_step(step, done_steps, order)


def do_step(step, done_steps, order):
    done_steps[step] = True
    order.append(step)
    return step


def do_step_2(step_list, order, step_prereqs, index=0):
    order.append(step_list[index])
    for i in step_prereqs:
        if step_list[index] in step_prereqs[i]:
            step_prereqs[i].remove(step_list[index])
            if len(step_prereqs[i]) < 1:
                step_list.append(i)
    step_list.pop(index)
    step_list.sort()

def part_1():
    step_dict, performed = make_step_list(input_file)
    step_dict_update = dict(step_dict)
    step_order = []
    # Create a list of steps that can be performed
    steps_available = [i for i in performed if i not in step_dict_update]
    # Perform earliest one in the list
    steps_available.sort()
    while len(step_order) < len(performed):
        do_step_2(steps_available, step_order, step_dict_update, 0)
    print(step_order)
    for i in step_order:
        print(i, end='')
    print()


# Part 2
def part_2(number_of_workers):
    workers = [['0', 0] for i in range(number_of_workers)]
    step_dict, performed = make_step_list(input_file)
    step_dict_update = dict(step_dict)
    step_order = []
    steps_available = [i for i in performed if i not in step_dict_update]
    steps_available.sort()
    timer = 0
    while len(step_order) < len(performed):
        timer += 1
        print('Timer:', timer, 'Worker report:', workers)
        # print('Steps available:', steps_available)
        for i in workers:
            if i[0] == '0' and len(steps_available) > 0:
                assign_worker(i, steps_available)
        update_workers(workers, 60, steps_available, step_order, step_dict_update)
    print('Timer:', timer)


def update_workers(workers, seconds_plus, step_list, step_order, step_prereqs):
    for i in workers:
        i[1] += 1
        if i[0] is not '0' and i[1] >= ord(i[0])-64+seconds_plus:
            step_order.append(i[0])
            for j in step_prereqs:
                if i[0] in step_prereqs[j]:
                    step_prereqs[j].remove(i[0])
                    if len(step_prereqs[j]) < 1:
                        step_list.append(j)
            i[0] = '0'
            i[1] = 0


def assign_worker(worker, steps):
    worker[0] = steps[0]
    worker[1] = 0
    steps.pop(0)


print([[i, ord(i)-64] for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']])
part_2(5)
