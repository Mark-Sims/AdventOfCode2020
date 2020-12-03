import os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
abs_input_filepath = os.path.join(script_dir, 'input.txt')

input = set()
input_list = []

with open(abs_input_filepath, 'r') as inputfp:
    line = inputfp.readline()
    while(line):
        input.add(int(line))
        input_list.append(int(line))
        line = inputfp.readline()

# Part 1
# for item in input:
#     if (2020 - item) in input:
#         print(item)
#         print(2020 - item)
#         print(item * (2020 - item))
#         break

# Part 2
for i in range(len(input_list)):
    for j in range(len(input_list)):
        first_candidate = input_list[i]
        second_candidate = input_list[j]
        third_candidate = ((2020 - first_candidate) - second_candidate)
        if third_candidate in input:
            print(first_candidate)
            print(second_candidate)
            print(third_candidate)
            print(first_candidate * second_candidate * third_candidate)