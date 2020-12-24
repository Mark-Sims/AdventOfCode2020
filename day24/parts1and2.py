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

tiles = AoCParser(abs_input_filepath).parse_as_list_of_strings()


def part_1():
    flipped_tiles = set()
    for tile in tiles:
        x_pos = 0
        y_pos = 0
        char_index = 0
        while char_index < len(tile):
            step = tile[char_index]
            if step == "e":
                x_pos += 2
            elif step == "w":
                x_pos -= 2
            else:
                char_index += 1
                second_step_char = tile[char_index]
                if step == "n":
                    if second_step_char == "e":
                        x_pos += 1
                        y_pos -= 1
                    else:
                        x_pos -= 1
                        y_pos -= 1
                else:
                    if second_step_char == "e":
                        x_pos += 1
                        y_pos += 1
                    else:
                        x_pos -= 1
                        y_pos += 1
            char_index += 1

        if (x_pos, y_pos) in flipped_tiles:
            flipped_tiles.remove((x_pos, y_pos))
        else:
            flipped_tiles.add((x_pos, y_pos))

    return flipped_tiles

flipped_tiles = part_1()
print(len(flipped_tiles))

# Part 2

def part_2(flipped_tiles, days):
    def get_neighbors(tile_coords):
        (x, y) = tile_coords
              #     E,          W, NE, NW, SE, SW
        return [
            (x + 2, y),     # E
            (x - 2, y),     # W
            (x + 1, y - 1), # NE
            (x - 1, y - 1), # NW
            (x + 1, y + 1), # SE
            (x - 1, y + 1)  # SW
        ]
    
    def count_living_neighbors(living_tiles, tile_coords):
        count = 0
        for neighbor in get_neighbors(tile_coords):
            if neighbor in living_tiles:
                count += 1

        return count

    def play_life(living_tiles):
        tiles_to_check = set()
        for tile in living_tiles:
            tiles_to_check.add(tile)
            tiles_to_check.update(get_neighbors(tile))

        next_day = set()
        for tile in tiles_to_check:
            living_neighbors = count_living_neighbors(living_tiles, tile)
            if tile in living_tiles:
                if living_neighbors == 1 or living_neighbors == 2:
                    next_day.add(tile)
            else:
                if living_neighbors == 2:
                    next_day.add(tile)

        return next_day

    day_counter = 1
    while day_counter <= days:
        flipped_tiles = play_life(flipped_tiles)
        print("Day {}: {}".format(day_counter, len(flipped_tiles)))
        day_counter += 1


part_2(flipped_tiles, 100)