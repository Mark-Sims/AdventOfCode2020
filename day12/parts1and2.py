import sys, os
import re

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser

abs_input_filepath = os.path.join(script_dir, 'input.txt')

navigation_instruction = AoCParser(abs_input_filepath).parse_as_list_of_strings()

# Part 1
# Use a counter, along with a modulo calculation determine the cardinal direction
# Cardinal Direction     Corresponding Remainder
#         N                         0
#       W   E                     3   1
#         S                         2
#

def part_1():
    direction_facing = 1
    x = 0
    y = 0
    for instruction_and_distance in navigation_instruction:
        instruction = re.findall("^[A-Z]", instruction_and_distance)[0]
        distance = int(re.findall("[0-9]+$", instruction_and_distance)[0])

        if instruction == "F":
            if direction_facing % 4 == 0:
                instruction = "N"
            elif direction_facing % 4 == 1:
                instruction = "E"
            elif direction_facing % 4 == 2:
                instruction = "S"
            elif direction_facing % 4 == 3:
                instruction = "W"

        if instruction == "N":
            y -= distance
        elif instruction == "E":
            x += distance
        elif instruction == "S":
            y += distance
        elif instruction == "W":
            x -= distance
        elif instruction == "L":
            direction_facing -= (distance / 90)
        elif instruction == "R":
            direction_facing += (distance / 90)


    print(abs(x) + abs(y))

def part_2():
    direction_facing = 1
    # Absolute position of the ship
    x = 0
    y = 0

    # Waypoint coords are relative to the ship
    waypoint_x = 10
    waypoint_y = -1
    for instruction_and_distance in navigation_instruction:
        instruction = re.findall("^[A-Z]", instruction_and_distance)[0]
        distance = int(re.findall("[0-9]+$", instruction_and_distance)[0])

        if instruction == "F":
            x += distance * waypoint_x
            y += distance * waypoint_y
        elif instruction == "N":
            waypoint_y -= distance
        elif instruction == "E":
            waypoint_x += distance
        elif instruction == "S":
            waypoint_y += distance
        elif instruction == "W":
            waypoint_x -= distance

        # Remove rotations that are identitical to allow us to simplify rotation code below
        if instruction == "R":
            instruction = "L"
            # R90 == L270
            if distance == 90:
                distance = 270
            # R270 == L90
            elif distance == 270:
                distance = 90

        if instruction == "L":
            if distance == 90:
                temp = waypoint_x
                waypoint_x = waypoint_y
                waypoint_y = temp * -1
            elif distance == 180:
                waypoint_x = -1 * waypoint_x
                waypoint_y = -1 * waypoint_y
            elif distance == 270:
                temp = waypoint_x
                waypoint_x = waypoint_y * -1
                waypoint_y = temp
    
    print(abs(x) + abs(y))

part_2()