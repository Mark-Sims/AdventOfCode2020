import sys, os
import re

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser

abs_input_filepath = os.path.join(script_dir, 'input.txt')

groups = AoCParser(abs_input_filepath).parse_as_list_of_paragraphs()

# Part 1
running_sum = 0
for group in groups:
    unique_answers = set()
    for passenger_survey in group:
        for passenger_answer in passenger_survey:
            unique_answers.add(passenger_answer)
    running_sum += len(unique_answers)

print(running_sum)

# Part 2
running_sum = 0
for group in groups:
    # Create a set from the first passenger's answers
    unique_answers = set([passenger_answer for passenger_answer in group.pop()])
    # Now we're only operating at the remaining passengers in this group
    for passenger_survey in group:
        # Create a copy of the set - one for iterating, and one for removing
        candidate_answers = [answer for answer in unique_answers]
        for candidate_answer in candidate_answers:
            if candidate_answer not in passenger_survey:
                unique_answers.remove(candidate_answer)

    running_sum += len(unique_answers)

print(running_sum)