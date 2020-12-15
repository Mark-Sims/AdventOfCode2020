import sys, os
import re
import operator
from functools import reduce

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser

abs_input_filepath = os.path.join(script_dir, 'input.txt')

starting_numbers = AoCParser(abs_input_filepath).parse_as_comma_separated_line_of_ints()

global_turn_counter = 1
history = {}

for starting_number in starting_numbers:
    history[starting_number] = [global_turn_counter]
    global_turn_counter += 1

last_number_spoken = starting_numbers[-1]
while global_turn_counter != 30000001:
    if len(history[last_number_spoken]) == 1:
        spoken_number = 0
    else:
        spoken_number = history[last_number_spoken][-1] - history[last_number_spoken][-2]

    # Setup our data structures/book keeping for the next turn
    if spoken_number in history:
        history[spoken_number].append(global_turn_counter)
    else:
        history[spoken_number] = [global_turn_counter]

    global_turn_counter += 1
    last_number_spoken = spoken_number

print(last_number_spoken)