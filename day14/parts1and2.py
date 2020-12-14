import sys, os
import re
import operator
from functools import reduce

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser

abs_input_filepath = os.path.join(script_dir, 'input.txt')

lines = AoCParser(abs_input_filepath).parse_as_list_of_strings()

cleaned_commands = []
for line in lines:
    split_command = line.split(" = ")
    if "mem" in split_command[0]:
        arg = re.findall("\d+", split_command[0])[0]
        cleaned_commands.append(["mem", int(arg), int(split_command[1])])
    else:
        cleaned_commands.append(["mask", split_command[1]])


# Part 1
def part_1():
    def apply_mask(mask, decimal_integer):
        binary = bin(decimal_integer).replace("0b", "").zfill(36)

        applied_mask = ""
        for bit_index in range(len(mask)):
            if mask[bit_index] == "0" or mask[bit_index] == "1":
                applied_mask += mask[bit_index]
            else:
                applied_mask += binary[bit_index]

        return int(applied_mask, 2)

    memory = {}
    mask = None
    for command in cleaned_commands:
        if command[0] == "mask":
            mask = command[1]
        else:
            memory[command[1]] = apply_mask(mask, command[2])

    print(sum(memory[key] for key in memory))

def part_2():
    memory = {}
    def write_to_mem(decimal_addr, mask, decimal_value):
        binary_addr = bin(decimal_addr).replace("0b", "").zfill(36)

        applied_mask = ""
        for bit_index in range(len(mask)):
            if mask[bit_index] == "0":
                applied_mask += binary_addr[bit_index]
            elif mask[bit_index] == "1":
                applied_mask += "1"
            else:
                mask = mask[:bit_index] + "0" + mask[bit_index + 1:]

                binary_addr_0 = binary_addr[:bit_index] + "0" + binary_addr[bit_index + 1:]
                binary_addr_1 = binary_addr[:bit_index] + "1" + binary_addr[bit_index + 1:]

                write_to_mem(int(binary_addr_0, 2), mask, decimal_value)
                write_to_mem(int(binary_addr_1, 2), mask, decimal_value)
                return

        memory[int(applied_mask, 2)] = decimal_value

    mask = ""
    for command in cleaned_commands:
        if command[0] == "mask":
            mask = command[1]
        else:
            write_to_mem(command[1], mask, command[2])

    print(sum(memory[key] for key in memory))

part_2()

