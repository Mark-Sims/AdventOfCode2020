import sys, os
import re

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser

abs_input_filepath = os.path.join(script_dir, 'input.txt')

rules = AoCParser(abs_input_filepath).parse_as_list_of_strings()
raw_instructions = []

# Part 1
for rule in rules:
    tokens = rule.split()
    operation = tokens[0]
    arg = int(tokens[1])
    raw_instructions.append((operation, arg))

def execute_program(instructions):
    instruction_pointer = 0
    accumulator = 0
    instructions_executed = set()
    while instruction_pointer not in instructions_executed:
        instructions_executed.add(instruction_pointer)
        operation = instructions[instruction_pointer][0]
        arg = instructions[instruction_pointer][1]

        if operation == "nop":
            instruction_pointer += 1
        elif operation == "acc":
            accumulator += arg
            instruction_pointer += 1
        elif operation == "jmp":
            instruction_pointer += arg
        
        if instruction_pointer == len(instructions):
            print("Program terminated. Accumulator: {}".format(accumulator))
            return

execute_program(raw_instructions)

# Part 2
for instruction_index in range(len(raw_instructions)):
    operation = raw_instructions[instruction_index][0]
    arg = raw_instructions[instruction_index][1]
    if operation == "acc":
        continue

    modified_instructions = raw_instructions.copy()
    if operation == "nop":
        modified_instructions[instruction_index] = ("jmp", arg)
    elif operation == "jmp":
        modified_instructions[instruction_index] = ("nop", arg)
    
    execute_program(modified_instructions)

        