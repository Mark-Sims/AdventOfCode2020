import sys, os
import re
import operator
from functools import reduce

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser

abs_input_filepath = os.path.join(script_dir, 'input.txt')

lines = AoCParser(abs_input_filepath).parse_as_list_of_strings()

current_timestamp = int(lines[0])
bus_ids = lines[1].split(',')

# Part 1
def part_1():
    # Remove the out of service bus_ids
    in_service_bus_ids = []
    for bus_id in bus_ids:
        if bus_id == "x":
            continue
        in_service_bus_ids.append(int(bus_id))

    in_service_bus_ids.sort()

    wait_time = 0
    while True:
        for in_service_bus in in_service_bus_ids:
            # Check if the bus departs at this timestamp
            if (current_timestamp + wait_time) % in_service_bus == 0:
                print(in_service_bus)
                print("Wait Time: {}".format(wait_time))
                raise
        wait_time += 1

#part_1()

# Part 2
def part_2_brute_force(bus_ids):
    iteration = 0
    for bus_id in bus_ids:
        timestamp = bus_id * iteration

    def find_earliest_timestamp(start_timestamp, bus_index):
        if bus_index == len(bus_ids):
            return True

        if bus_ids[bus_index] == "x":
            return find_earliest_timestamp(start_timestamp, bus_index + 1)

        if (start_timestamp + bus_index) % int(bus_ids[bus_index]) == 0:
            return find_earliest_timestamp(start_timestamp, bus_index + 1)

        return False


    iteration = 0
    while not find_earliest_timestamp(int(bus_ids[0]) * iteration, 0):
        iteration += 1

    print(iteration * int(bus_ids[0]))

#part_2_brute_force(bus_ids)

def prod(factors):
    return reduce(operator.mul, factors, 1)

def part_2_efficient():
    in_service_bus_ids_with_index = []
    for bus_index in range(len(bus_ids)):
        if bus_ids[bus_index] != 'x':
            in_service_bus_ids_with_index.append( (int(bus_ids[bus_index]), bus_index) )

    def detect_offset_in_cycle(tuple_a, tuple_b):
        cycle_distance = tuple_a[0] * tuple_b[0]
        print("{} and {} cycle every {}".format(tuple_a[0], tuple_b[0], cycle_distance))

        offset_amount = tuple_b[1] - tuple_a[1]
        a_multiplier = 1
        b_multiplier = 1
        while a_multiplier * tuple_a[0] < cycle_distance:
            a_total = a_multiplier * tuple_a[0]
            b_total = b_multiplier * tuple_b[0]
            if b_total - a_total == offset_amount:
                print("Sequence starts at {}".format(tuple_a[0] * a_multiplier))
                print("a_multiplier: {}        b_multiplier: {}".format(a_multiplier, b_multiplier))
                print("-----------")
                return tuple_a[0] * a_multiplier

            if a_total < b_total:
                a_multiplier += 1

            if b_total < a_total:
                b_multiplier += 1

            # Means we hit a cycle. This should have been caught, and pre-empted by the loop condition
            if a_total == b_total:
                raise

    step_size = 1
    candidate = 1
    for i in range(len(in_service_bus_ids_with_index) - 1):
        a = in_service_bus_ids_with_index[i]
        b = in_service_bus_ids_with_index[i + 1]

        print("Stepping by {}'s".format(step_size))

        while True:
            if (candidate + a[1]) % a[0] == 0 and (candidate + b[1]) % b[0] == 0:
                print("Found candidate {} for bus ids: {} and {}".format(candidate, a[0], b[0]))
                step_size = prod(pair[0] for pair in in_service_bus_ids_with_index[0:i + 2])
                break
            candidate += step_size

part_2_efficient()