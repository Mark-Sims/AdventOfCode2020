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

public_keys = AoCParser(abs_input_filepath).parse_as_list_of_ints()

card_public_key = public_keys[0]
door_public_key = public_keys[1]

# Part 1
def part_1():
    value = 1

    def transform(value, subject_number):
        value *= subject_number
        return value % 20201227

    secret_loop_counter = 0
    while value != card_public_key:
        value = transform(value, 7)
        secret_loop_counter += 1

    card_secret_loop_size = secret_loop_counter

    print("Card secret loop size: {}".format(card_secret_loop_size))

    value = 1
    secret_loop_counter = 0
    while value != door_public_key:
        value = transform(value, 7)
        secret_loop_counter += 1

    door_secret_loop_size = secret_loop_counter
    print("Door secret loop size: {}".format(door_secret_loop_size))

    value = 1
    i = 0
    while i < card_secret_loop_size:
        value = transform(value, door_public_key)
        i += 1

    print(value)

part_1()