import sys, os
import re
import operator
from functools import reduce
import math

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser, prod

abs_input_filepath = os.path.join(script_dir, 'input.txt')

raw_tiles = AoCParser(abs_input_filepath).parse_as_list_of_paragraphs()

# Part 1

side_length = 10

class Tile:
    def __init__(self, tile_paragraph):
        self.tile_id = re.findall("[0-9]+", tile_paragraph[0])[0]
        self.grid = tile_paragraph[1:]
        self.orientation_locked = False
        self.num_matched_neighbors = 0
        self.neighbors = []
        self.calculate_side_values()

    def calculate_side_values(self):
        self.north_border = Tile.convert_to_decimal(self.grid[0])
        self.east_border = Tile.convert_to_decimal("".join([row[-1] for row in self.grid]))
        self.south_border = Tile.convert_to_decimal(self.grid[-1])
        self.west_border = Tile.convert_to_decimal("".join([row[0] for row in self.grid]))

        self.all_borders = [self.north_border, self.east_border, self.south_border, self.west_border]
    
    def print_tile(self):
        for row in self.grid:
            string = ""
            for col in row:
                string += col + " "
            print(string)

    def flip_horizontally(self, recalculate_side_values=True):
        if self.orientation_locked:
            return
        new_grid = []
        for row in self.grid:
            new_grid.append(row[::-1])
        self.grid = new_grid

        if recalculate_side_values:
            self.calculate_side_values()

    def flip_vertically(self, recalculate_side_values=True):
        if self.orientation_locked:
            return
        new_grid = []
        for row in self.grid[::-1]:
            new_grid.append(row)
        self.grid = new_grid
        if recalculate_side_values:
            self.calculate_side_values()

    def rotate_90_clockwise(self, recalculate_side_values=True):
        self.grid[::-1] # This line does nothing...
        tuples_grid = list(zip(*self.grid))
        self.grid = ["".join(i) for i in [j for j in tuples_grid]]
        # Not sure why I need to do this flip here...
        self.flip_horizontally(recalculate_side_values)

    def rotate_180(self):
        self.rotate_90_clockwise(False)
        self.rotate_90_clockwise()

    def rotate_90_counterclockwise(self):
        self.rotate_90_clockwise(False)
        self.rotate_90_clockwise(False)
        self.rotate_90_clockwise()

    # Represent a row as a binary string where
    # "#" = 1 and "." = 0
    # Then convert that binary string to a decimal number
    def convert_to_decimal(string):
        string = string.replace("#", "1")
        string = string.replace(".", "0")
        return int(string, 2)

    # Part 2
    def remove_borders(self):
        self.grid = self.grid[1:-1]
        self.grid = [row[1:-1] for row in self.grid]

tiles = []
tiles_dict = {}
for tile in raw_tiles:
    tiles.append(Tile(tile))
    tiles_dict[tiles[-1].tile_id] = tiles[-1]

sides = {} # side value -> list of tile_id's which contain that side value

def add_sides(tile):
    for border in tile.all_borders:
        if border in sides:
            sides[border].append(tile.tile_id)
        else:
            sides[border] = [tile.tile_id]

def remove_sides(tile):
    for border in tile.all_borders:
        if len(sides[border]) == 1:
            sides.pop(border)
        else:
            sides[border].remove(tile.tile_id)

for tile in tiles:
    add_sides(tile)

#def count_neighbors(tile):
#    num_of_tiles_with_common_borders = 0
#    for border in tile.all_borders:
#        num_of_tiles_with_common_borders += int(len(sides[border]) / 2)
#    return num_of_tiles_with_common_borders
#
#def get_neighbors(tile):
#    neighbors = []
#    for border in tile.all_borders:
#        neighbors += [i for i in sides[border] if i != tile.tile_id]
#    return neighbors

    #if num_of_tiles_with_common_borders > 0:
    #    for t in sides[border]:
    #        tiles_dict[t].orientation_locked = True
    #        tiles_dict[t].num_matched_neighbors = num_of_tiles_with_common_borders


# Unused
#for tile in tiles:
#    tile.num_matched_neighbors = count_neighbors(tile)
#    tile.neighbors = get_neighbors(tile)

#before = len(sides)
#after = 0
#while before != after:
#    before = len(sides)
#    print(len(sides))
#    for tile in tiles:
#        if tile.orientation_locked:
#            continue
#        if tile.num_matched_neighbors == 0:
#            for border in tile.all_borders:
#                if len(sides[border]) == 1:
#                    sides.pop(border)
#                else:
#                    sides[border].remove(tile.tile_id)
#            tile.flip_horizontally()
#            add_sides(tile)
#            tally_neighbors(tile)
#        elif tile.num_matched_neighbors == 4:
#            for side in tile.all_borders:
#                for t in sides[side]:
#                    print("Locking tile {}".format(t))
#                    tiles_dict[t].orientation_locked = True
#    after = len(sides)
#
#before = len(sides)
#after = 0
#while before != after:
#    before = len(sides)
#    print(len(sides))
#    for tile in tiles:
#        if tile.orientation_locked:
#            continue
#        if tile.num_matched_neighbors == 0:
#            for border in tile.all_borders:
#                if len(sides[border]) == 1:
#                    sides.pop(border)
#                else:
#                    sides[border].remove(tile.tile_id)
#            tile.flip_vertically()
#            add_sides(tile)
#            tally_neighbors(tile)
#        elif total_matching_sides == 8:
#            for side in tile.all_borders:
#                for t in sides[side]:
#                    print("Locking tile {}".format(t))
#                    tiles_dict[t].orientation_locked = True
#
#    after = len(sides)
#
#locked_tiles = [tile.tile_id for tile in tiles if tile.orientation_locked]

#tiles_with_2_unmatched_borders = []
#for tile in tiles:
#    num_unmatched_borders = 0
#    for border in tile.all_borders:
#        if len(sides[border]) == 1:
#            num_unmatched_borders += 1
#    if num_unmatched_borders == 2:
#        tiles_with_2_unmatched_borders.append(tile)

#def print_summary():
#    for i in range(5):
#        print("{} tiles with {} neighbors".format(len([t for t in tiles if t.num_matched_neighbors == i]), i))
#    print("---------------------")
#
#print_summary()
#
#tiles_without_neighbors = [t for t in tiles if t.num_matched_neighbors == 0]
#for tile in tiles_without_neighbors:
#    remove_sides(tile)
#    tile.flip_horizontally()
#    add_sides(tile)
#    tile.num_matched_neighbors = count_neighbors(tile)
#
#print_summary()

# Unused
def flip_tile(tile):
    tile.flip_horizontally()
    flipped_tile_ids = set([tile.tile_id])
    tiles_to_flip = tile.neighbors
    while len(tiles_to_flip) > 0:
        tile_id = tiles_to_flip.pop()
        if tile_id in flipped_tile_ids:
            continue
        tiles_dict[tile_id].flip_horizontally()
        flipped_tile_ids.add(tile_id)
        tiles_to_flip += tiles_dict[tile_id].neighbors

# Unused
def flip_all_cards(num_neighbors):
    tiles_without_neighbors = [t for t in tiles if t.num_matched_neighbors == num_neighbors]
    for tile in tiles_without_neighbors:
        flip_tile(tile)
    print_summary()

def compliment(decimal):
    binary = bin(decimal).replace("0b", "")
    binary = binary.zfill(10)
    binary = binary[::-1]
    return int(binary, 2)



def find_tile_with_matching_edge(start_tile_id, search_edge):
    if search_edge in sides:
        if len([i for i in sides[search_edge] if i != start_tile_id]) == 1:
            return [i for i in sides[search_edge] if i != start_tile_id][0]
        else:
            compliment_of_search_edge = compliment(search_edge)
            if compliment_of_search_edge in sides:
                found_tile_id = [i for i in sides[compliment_of_search_edge] if i != start_tile_id][0]
                print("Need to flip tile with id {}".format(found_tile_id))
                found_tile = tiles_dict[found_tile_id]
                remove_sides(found_tile)
                if compliment_of_search_edge in [found_tile.east_border, found_tile.west_border]:
                    found_tile.flip_vertically()
                else:
                    found_tile.flip_horizontally()
                add_sides(found_tile)
                return found_tile_id
            raise Exception
    else:
        print("THIS SHOULDN'T HAPPEN! IT MEANS THERE IS AN EDGE VALUE THAT DOESN'T EXIST IN SIDES")

# [N, E, S, W]
def step(start, direction):
    if direction == 'N':
        try:
            next_tile_id = find_tile_with_matching_edge(start.tile_id, start.north_border)
        except:
            print("Cannot step further North")
            return start
        next_tile = tiles_dict[next_tile_id]
        remove_sides(next_tile)
        if start.north_border == next_tile.south_border:
            pass
        elif start.north_border == next_tile.north_border:
            next_tile.flip_vertically()
        elif start.north_border == next_tile.west_border:
            next_tile.rotate_90_counterclockwise()
        else:
            next_tile.rotate_90_clockwise()
            next_tile.flip_horizontally()

        # Quick sanity check
        if start.grid[0] != next_tile.grid[-1]:
            print(start.grid[0])
            print(next_tile.grid[-1])
            raise

        add_sides(next_tile)
        return next_tile
    if direction == 'S':
        try:
            next_tile_id = find_tile_with_matching_edge(start.tile_id, start.south_border)
        except:
            print("Cannot step further South")
            return start
        next_tile = tiles_dict[next_tile_id]
        remove_sides(next_tile)
        if start.south_border == next_tile.north_border:
            pass
        elif start.south_border == next_tile.west_border:
            next_tile.rotate_90_clockwise()
            next_tile.flip_horizontally()
        elif start.south_border == next_tile.east_border:
            next_tile.rotate_90_counterclockwise()
        else:
            next_tile.flip_vertically()

        # Quick sanity check
        if start.grid[-1] != next_tile.grid[0]:
            print(start.grid[-1])
            print(next_tile.grid[0])
            raise
        
        add_sides(next_tile)
        return next_tile

    if direction == 'E': # untested
        try:
            next_tile_id = find_tile_with_matching_edge(start.tile_id, start.east_border)
        except:
            print("Cannot step further East")
            return start
        next_tile = tiles_dict[next_tile_id]
        remove_sides(next_tile)
        if start.east_border == next_tile.west_border:
            pass
        elif start.east_border == next_tile.north_border:
            next_tile.rotate_90_counterclockwise()
            next_tile.flip_vertically()
        elif start.east_border == next_tile.east_border:
            next_tile.flip_horizontally()
        else:
            next_tile.rotate_90_clockwise()

        # Quick sanity check
        east_side_of_start_tile = "".join([row[-1] for row in start.grid])
        west_side_of_next_tile = "".join([row[0] for row in next_tile.grid])
        if east_side_of_start_tile != west_side_of_next_tile:
            print(east_side_of_start_tile)
            print(west_side_of_next_tile)
            raise

        add_sides(next_tile)
        return next_tile

    if direction == 'W':
        try:
            next_tile_id = find_tile_with_matching_edge(start.tile_id, start.west_border)
        except:
            print("Cannot step further West")
            return start
        next_tile = tiles_dict[next_tile_id]
        remove_sides(next_tile)
        if start.west_border == next_tile.east_border:
            pass
        elif start.west_border == next_tile.north_border:
            next_tile.rotate_90_clockwise()
        elif start.west_border == next_tile.west_border:
            next_tile.flip_horizontally()
        else:
            next_tile.rotate_90_counterclockwise()
            next_tile.flip_vertically()

        # Quick sanity check
        west_side_of_start_tile = "".join([row[0] for row in start.grid])
        east_side_of_next_tile = "".join([row[-1] for row in next_tile.grid])
        if west_side_of_start_tile != east_side_of_next_tile:
            print(west_side_of_start_tile)
            print(east_side_of_next_tile)
            raise

        add_sides(next_tile)
        return next_tile


# Part 2
# My input tiles:
top_left = tiles_dict["1699"]

# Example tiles:
#top_left = tiles_dict["2971"]
# Requires flip vertically, rotate 90 clockwise, flip horizontally
#full_image = flip_image_vertically(full_image)
#full_image = rotate_image_90_clockwise(full_image)
#full_image = flip_image_horizontally(full_image)

grid_side_length = int(math.sqrt(len(tiles_dict)))
y = 0
grid_of_tiles = []
while y < grid_side_length:
    position = top_left
    for i in range(y):
        position = step(position, 'S')
    x = 0
    row = []
    while x < grid_side_length:
        row.append(position.tile_id)
        position = step(position, 'E')
        x += 1
    y += 1
    grid_of_tiles.append(row)

# Merges the tiles (containing lists of strings) into a single list of strings
def merge_full_grid(grid_of_tiles, strip_borders=True, include_gridlines=False):
    full_image = []
    for tile_row in grid_of_tiles:
        merged_image_row = []
        for tile_id in tile_row:
            tile = tiles_dict[tile_id]
            if strip_borders:
                tile.remove_borders()
            for tile_row_index in range(len(tile.grid)):
                if len(merged_image_row) < len(tile.grid):
                    # This is our first pass, add the tile row
                    if include_gridlines:
                        merged_image_row.append(tile.grid[tile_row_index] + "|")
                    else:
                        merged_image_row.append(tile.grid[tile_row_index])
                else:
                    if include_gridlines:
                        merged_image_row[tile_row_index] += tile.grid[tile_row_index] + "|"
                    else:
                        merged_image_row[tile_row_index] += tile.grid[tile_row_index]
        if include_gridlines:
            merged_image_row.append("-" * len(merged_image_row[0]))
        full_image += merged_image_row
    return full_image
            
full_image = merge_full_grid(grid_of_tiles, strip_borders=True, include_gridlines=False)

def rotate_image_90_clockwise(image):
    image = image[::-1]
    image = list(zip(*image))
    return ["".join(i) for i in [j for j in image]]

def flip_image_horizontally(image):
    new_image = []
    for row in image:
        new_image.append(row[::-1])
    return new_image

def flip_image_vertically(image):
    new_image = []
    for row in image[::-1]:
        new_image.append(row)
    return new_image

# Used trial and error for flipping, and rotating the grid until I found
# an orientation that contained sea monsters
full_image = flip_image_horizontally(full_image)
full_image = rotate_image_90_clockwise(full_image)
full_image = rotate_image_90_clockwise(full_image)

#                01234567890123456789
sea_monster_1 = "                  # "
sea_monster_2 = "#    ##    ##    ###"
sea_monster_3 = " #  #  #  #  #  #   "

# I messed these up, and they're actually (y, x)
sea_monster_body_part_offsets = [
    (0, 18),
    (1, 0), (1, 5), (1, 6), (1, 11), (1, 12), (1, 17), (1, 18), (1, 19), 
    (2, 1), (2, 4), (2, 7), (2, 10), (2, 13), (2, 16)
]

sea_monster_1_regex = sea_monster_1.replace(" ", ".")
sea_monster_2_regex = sea_monster_2.replace(" ", ".")
sea_monster_3_regex = sea_monster_3.replace(" ", ".")

def check_for_sea_monster(x, y):
    first_row_candidate = full_image[y][x:x + len(sea_monster_1_regex)]
    if re.match(sea_monster_1_regex, first_row_candidate):
        second_row_candidate = full_image[y + 1][x:x + len(sea_monster_2_regex)]
        if re.match(sea_monster_2_regex, second_row_candidate):
            third_row_candidate = full_image[y + 2][x:x + len(sea_monster_3_regex)]
            if re.match(sea_monster_3_regex, third_row_candidate):
                return True
    return False

sea_monster_coordinates = []
for row_index in range(len(full_image)):
    row = full_image[row_index]
    if len(full_image) - row_index < 3:
        # Don't have room below
        #print("Breaking at y = {}".format(row_index))
        break
    for col_index in range(len(row)):
        if len(row) - col_index < 20:
            # Don't have room to the right
            #print("Breaking at x = {}".format(col_index))
            break
        if check_for_sea_monster(col_index, row_index):
            sea_monster_coordinates.append((col_index, row_index))

print("Sea monsters located at the following coordinates: {}".format(sea_monster_coordinates))

# Convert the image from a list of strings to a list of lists so that I can re-assign individual cells
# without re-creating a string for the entire row, and replaceing that row.
assignable_full_image = []
for row in full_image:
    assignable_row = []
    assignable_row[:] = row
    assignable_full_image.append(assignable_row)

a = 5

# Re-assign cells where a sea-monster is located with a "O"
def block_out_sea_monster(coords):
    (x, y) = coords
    for body_part in sea_monster_body_part_offsets:
        (body_part_y_offset, body_part_x_offset) = body_part
        assignable_full_image[y + body_part_y_offset][x + body_part_x_offset] = "O"

# Block out every sea monster
for sea_monster in sea_monster_coordinates:
    block_out_sea_monster(sea_monster)

# Count the number of "#" left in the grid
hash_count = 0
for row in assignable_full_image:
    for cell in row:
        if cell[0] == "#":
            hash_count += 1

print(hash_count)


