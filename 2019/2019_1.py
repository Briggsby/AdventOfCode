import math
import functools

input = open("./2019/2019_1_input.txt", 'r').read().splitlines()

total = 0

for element in input:
    fuel_requirement =  math.floor(int(element)/3)-2
    total += fuel_requirement

print(total)


def calculate_fuel(mass):
    fuel = max(0, math.floor(mass/3)-2)
    extra_fuel = max(0, calculate_fuel(fuel)) if fuel > 6 else 0
    return fuel+extra_fuel


total = 0

for element in input:
    fuel_requirement = calculate_fuel(int(element))
    total += fuel_requirement

print(total)