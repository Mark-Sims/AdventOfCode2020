import sys, os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser

abs_input_filepath = os.path.join(script_dir, 'input.txt')

seat_map = AoCParser(abs_input_filepath).parse_as_2d_list()

# Part 1

def count_occupied_neighbors(map, x, y):
    neighbor_count = 0

    # Check neighbors in the following clockwise order
    #
    # 1  2  3
    # 8     4
    # 7  6  5

    # 1
    if x > 0 and y > 0 and map[y - 1][x - 1] == '#':
        neighbor_count += 1
    # 2 
    if y > 0 and map[y - 1][x] == "#":
        neighbor_count += 1
    # 3
    if x < (len(map[0]) - 1) and y > 0 and map[y - 1][x + 1] == "#":
        neighbor_count += 1
    # 4
    if x < (len(map[0]) - 1) and map[y][x + 1] == "#":
        neighbor_count += 1
    # 5
    if x < (len(map[0]) - 1) and y < (len(map) - 1) and map[y + 1][x + 1] == "#":
        neighbor_count += 1
    # 6
    if y < (len(map) - 1) and map[y + 1][x] == "#":
        neighbor_count += 1
    # 7
    if x > 0 and y < (len(map) - 1) and map[y + 1][x - 1] == "#":
        neighbor_count += 1
    # 8
    if x > 0 and map[y][x - 1] == "#":
        neighbor_count += 1

    return neighbor_count

def run_game_of_life(seat_map):
    num_seat_changes = 1

    while num_seat_changes > 0: 
        num_seat_changes = 0
        new_seat_map = [y.copy() for y in seat_map]

        y = 0
        while y < len(seat_map):
            x = 0
            while x < len(seat_map[0]):
                occupied_neighbors = count_occupied_neighbors(seat_map, x, y)
                if seat_map[y][x] == "L" and occupied_neighbors == 0:
                    new_seat_map[y][x] = "#"
                    num_seat_changes += 1
                elif seat_map[y][x] == "#" and occupied_neighbors >= 4:
                    new_seat_map[y][x] = "L"
                    num_seat_changes += 1
                x += 1
            y += 1

        seat_map = new_seat_map
        print("Seat changes: {}".format(num_seat_changes))

    occupied_seats = 0
    for row in seat_map:
        for col in row:
            if col == "#":
                occupied_seats += 1

    print(occupied_seats)

run_game_of_life(seat_map)

# Part 2

def check_cell(map, x, y):
    try:
        # Python allows negative array indexing. Disallow that here.
        if x < 0 or y < 0:
            raise IndexError
        return map[y][x]
    except IndexError:
        # Treat the edge of the map as if it were an empty seat
        return "L"

# Multipliers are -1, 0, 1
def search_for_seat(map, x, x_direction_multiplier, y, y_direction_multiplier):
    step_distance = 1
    while step_distance < max(len(map), len(map[0])):
        seat_contents = check_cell(map, x + (step_distance * x_direction_multiplier), y + (step_distance * y_direction_multiplier))
        if seat_contents == ".":
            step_distance += 1
            continue
        return seat_contents


def count_occupied_neighbors_at_distance(map, x, y):
    neighbor_count = 0

    # Check neighbors in the following clockwise order
    #
    # 1  2  3
    # 8     4
    # 7  6  5

    # 1
    if search_for_seat(map, x, -1, y, -1) == '#':
        neighbor_count += 1
    # 2 
    if search_for_seat(map, x, 0, y, -1) == '#':
        neighbor_count += 1
    # 3
    if search_for_seat(map, x, 1, y, -1) == '#':
        neighbor_count += 1
    # 4
    if search_for_seat(map, x, 1, y, 0) == '#':
        neighbor_count += 1
    # 5
    if search_for_seat(map, x, 1, y, 1) == '#':
        neighbor_count += 1
    # 6
    if search_for_seat(map, x, 0, y, 1) == '#':
        neighbor_count += 1
    # 7
    if search_for_seat(map, x, -1, y, 1) == '#':
        neighbor_count += 1
    # 8
    if search_for_seat(map, x, -1, y, 0) == '#':
        neighbor_count += 1

    return neighbor_count

print(count_occupied_neighbors_at_distance(seat_map, 3, 3))

def run_game_of_life_part_2(seat_map):
    num_seat_changes = 1

    while num_seat_changes > 0: 
        num_seat_changes = 0
        new_seat_map = [y.copy() for y in seat_map]

        y = 0
        while y < len(seat_map):
            x = 0
            while x < len(seat_map[0]):
                occupied_neighbors = count_occupied_neighbors_at_distance(seat_map, x, y)
                if seat_map[y][x] == "L" and occupied_neighbors == 0:
                    new_seat_map[y][x] = "#"
                    num_seat_changes += 1
                elif seat_map[y][x] == "#" and occupied_neighbors >= 5:
                    new_seat_map[y][x] = "L"
                    num_seat_changes += 1
                x += 1
            y += 1

        seat_map = new_seat_map
        print("Seat changes: {}".format(num_seat_changes))

    occupied_seats = 0
    for row in seat_map:
        for col in row:
            if col == "#":
                occupied_seats += 1

    print(occupied_seats)

run_game_of_life_part_2(seat_map)