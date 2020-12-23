import sys, os
import re
import operator
from functools import reduce
import math
from collections import deque
from itertools import cycle

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser, prod

abs_input_filepath = os.path.join(script_dir, 'input.txt')

input_cups = AoCParser(abs_input_filepath).parse_as_single_line_of_undelimited_ints()

def part_1(cups, iterations):

    def remove_3_cups(current_cup_index):
        cup_indices = [current_cup_index + i for i in [1, 2, 3]]
        cup_indices = [cup_index % len(cups) for cup_index in cup_indices]
        removed_cups = [cups[i] for i in cup_indices]
        [cups.remove(cup) for cup in removed_cups]
        return removed_cups
    
    def get_destination_cup(current_cup):
        cups_less_than_current_cup = [cup for cup in cups if cup < current_cup]
        if len(cups_less_than_current_cup) == 0:
            return max(cups)
        return max(cups_less_than_current_cup)

    current_cup_index = 0
    current_cup = cups[current_cup_index]

    num_cups = len(cups)
    while iterations > 0:

        cup_strings = []
        for cup in cups:
            if cup == current_cup:
                cup_strings.append("({})".format(cup))
            else:
                cup_strings.append(str(cup))
        #print(cup_strings)
        pick_up = remove_3_cups(current_cup_index)
        #print(pick_up)
        destination_cup = get_destination_cup(current_cup) # inefficient
        #print(destination_cup)
        destination_cup_index = cups.index(destination_cup) # inefficient
        cups = cups[:destination_cup_index + 1] + pick_up + cups[destination_cup_index + 1:]

        # Prepare for next iteration
        current_cup_index = (cups.index(current_cup) + 1) % num_cups
        current_cup = cups[current_cup_index]

        iterations -= 1

    print(cups)

#part_1(input_cups.copy(), 100)

# Part 2

# Let's just try a brute force to see if it works...
#input_cups.extend(range(10, 1000001))
#part_1(input_cups, 10000000)
# Wow, yeah, that's not going to work. It takes a handful of seconds per iteration.
# With 10 million iterations, that's gonna be a while....

# Idea: Use a linked list for O(1) insertions/deletions in the middle of the list
# However, this still poses the issue of having to search O(n) find the "destionation cup"
# I could maintain some auxilary data structure (a map) which maintains a reference to that Node
# in the linked list. That way, I can lookup a Node in O(1) jump to it, and then immediately
# insert before/after it or remove it or whatever.
def part_2(cups, iterations, max_cup_value):
    class Node:
        def __init__(self, val, prev=None):
            self.val = val
            self.prev = prev
            self.next = None

        def __repr__(self):
            if self.prev and self.next:
                return "[{} -> {} -> {}]".format(self.prev.val, self.val, self.next.val)
            if self.prev:
                return "[{} -> {} -> None]".format(self.prev.val, self.val)
            if self.next:
                return "[None -> {} -> {}]".format(self.val, self.next.val)
            else:
                return "[None -> {} -> None]".format(self.val)

    cups_dictionary = {}

    if len(cups) == 0:
        raise Exception("No cups!")
        
    first_cup = Node(cups[0])
    previous_cup = first_cup
    cups_dictionary[cups[0]] = previous_cup
    for cup_val in cups[1:]:
        current_cup = Node(cup_val, previous_cup)
        cups_dictionary[cup_val] = current_cup
        previous_cup.next = current_cup
        previous_cup = current_cup

    # Connect the first and the last cups to make it a circularly linked list
    first_cup.prev = previous_cup
    previous_cup.next = first_cup

    def pick_up_next_3_cups(current_cup):
        ret = (current_cup.next, current_cup.next.next.next)
        current_cup.next = current_cup.next.next.next.next
        current_cup.next.prev = current_cup
        return ret

    def calculate_destination_value(current_cup_value, head_of_picked_up_cups):
        picked_up_cup_values = [
            head_of_picked_up_cups.val,
            head_of_picked_up_cups.next.val,
            head_of_picked_up_cups.next.next.val
        ]

        ret = None
        ret = current_cup_value - 1
        while ret == 0 or ret in picked_up_cup_values:
            if ret == 0:
                ret = max_cup_value
                continue
            ret -= 1

        return ret

    def print_cup_order(start_cup_value, length):
        cup_values = []
        cur = cups_dictionary[start_cup_value]
        while length > 0:
            cup_values.append(cur.val)
            cur = cur.next
            length -= 1

        print(", ".join([str(v) for v in cup_values]))


    current_cup = cups_dictionary[cups[0]]
    while iterations > 0:
        (pick_up_start_cup, pick_up_end_cup) = pick_up_next_3_cups(current_cup)
        destination_value = calculate_destination_value(current_cup.val, pick_up_start_cup)
        destination_cup = cups_dictionary[destination_value]
        temp = destination_cup.next

        destination_cup.next = pick_up_start_cup
        pick_up_start_cup.prev = destination_cup

        pick_up_end_cup.next = temp
        temp.prev = pick_up_end_cup

        # Select the next cup
        current_cup = current_cup.next

        iterations -= 1


    z = 0
    
input_cups.extend(range(10, 1000001))
part_2(input_cups, 10000000, 1000000)

# 149245887792 is too low

