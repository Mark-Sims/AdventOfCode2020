import sys, os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser

abs_input_filepath = os.path.join(script_dir, 'input.txt')

encoding = AoCParser(abs_input_filepath).parse_as_list_of_ints()

# Part 1
def solve_part_1():
    lookback_distance = 25

    i = lookback_distance
    while i < len(encoding):
        sum_to = encoding[i]
        j = 1
        found_match = False
        while j <= lookback_distance:
            first_candidate = encoding[i - j]
            search_for = sum_to - first_candidate
            if search_for in encoding[i - lookback_distance:i]:
                print("First num: {}".format(first_candidate))
                print("Second num: {}".format(search_for))
                print("Sum to: {}".format(sum_to))
                print("Search space {}".format(encoding[i - lookback_distance:i]))
                found_match = True
                break
            j += 1

        if not found_match:
            return encoding[i]
        i += 1

print("Couldn't find a pair adding up to {}".format(solve_part_1()))

# Part 2

# Brute Force
def solve_part_2():
    search_for = 69316178
    i = 0
    while i < len(encoding):
        sum = encoding[i]
        j = i + 1
        while j < len(encoding):
            sum += encoding[j]
            if sum == search_for:
                return encoding[i:j]
            j += 1
        i += 1

part_2 = solve_part_2()
print(part_2)
print(min(part_2) + max(part_2))

