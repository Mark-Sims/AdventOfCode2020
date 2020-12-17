import sys, os
import re
import operator
from functools import reduce

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser, prod

abs_input_filepath = os.path.join(script_dir, 'input.txt')

input_grid = AoCParser(abs_input_filepath).parse_as_2d_list()

# IDEA 1
# Idea 1 is to just simulate dead and living cells using a 3d matrix
# This should work fine sice for Part 1, we're only simulating 6
# "days" in the game of life. So the most the grid can expand is
# 6 * 2 = 12 in each dimension. 12 x 12 x 12 = 1728. That's plenty
# small enough to fit in memory, so we can simulate all cells, living
# and dead in memory. I'm worried though, that if I implement this
# naive solution, part 2 is going to come along and ask me to simulate
# 100,000,000 "days" in the game of life. In which case, simulating
# all living and dead cells in memory might not be feasible since the
# living cells (the only cells we really care about) might be incredibly
# sparse throughout that 3d space.

# IDEA 2
# Idea 2 involves using a series of nested dictionaries for the quick
# lookup of living cells. The dict at the first level maps x coordinate
# to the dictionary of y coordinates at that x coordinate. The dict at
# that second level, maps the y coordinate to the dictionary of z
# coordinates at those aforementioned x and y coordinates. I'm actually
# not positive that this will work either... at least not cleanly.
# This should work for detecting which cells will die, but it becomes
# much more complicated when we're trying to determine which cells
# come to life... My dictionary contains all cells that are living, but
# then I'd need to somehow check if each neighbor of each living
# cell has 3 or more living neighbors. This might produce a lot
# of redundant checking... Though... I might be able to memoize
# the cells I've already checked just using a set of (x, y, z)
# tuples. Actually... that gives me another idea, even easier, and
# hopefully way more efficient than this nested dictionary nonsense.

# IDEA 3 
# Idea 3 is to just maintain a single set of unique tuples that
# represent the (x, y, z) coordinates of living cells. Then when I want
# to check how many neighbors of a given cell are living, it's just a
# matter of generating the coords of each of the 27 neighbors - O(1), 
# and checking if those coords appear in the living cell set O(1). 
# Total time and space complexity are both O(n) with the number of
# living cells.


# Part 1
def part_1():
    # Build up the initial set of living cells
    living_cells = set()

    for y in range(len(input_grid)):
        for x in range(len(input_grid[0])):
            if input_grid[y][x] == "#":
                living_cells.add((x, y, 0))

    def generate_neighbors_3d(cell_coordinates, include_self=False):
        neighbor_offsets = set([
            (0, 0, 1),
            (0, 1, 0),
            (0, 1, 1),
            (1, 0, 0),
            (1, 0, 1),
            (1, 1, 0),
            (1, 1, 1),

            (0, 0, -1),
            (0, -1, 0),
            (0, -1, -1),
            (-1, 0, 0),
            (-1, 0, -1),
            (-1, -1, 0),
            (-1, -1, -1),

            (1, 1, -1),
            (1, -1, 1),
            (1, -1, -1),
            (-1, 1, 1),
            (-1, 1, -1),
            (-1, -1, 1),

            (0, 1, -1),
            (0, -1, 1),
            (1, 0, -1),
            (-1, 0, 1),
            (1, -1, 0),
            (-1, 1, 0),
        ])

        if include_self:
            neighbor_offsets.add((0, 0, 0))

        neighbors = []
        for neighbor_offset in neighbor_offsets:
            neighbor_x = cell_coordinates[0] + neighbor_offset[0]
            neighbor_y = cell_coordinates[1] + neighbor_offset[1]
            neighbor_z = cell_coordinates[2] + neighbor_offset[2]
            neighbors.append((neighbor_x, neighbor_y, neighbor_z))

        return neighbors

    def count_living_neighbors(all_living_cells, cell_coordinates):
        num_living_neighbors = 0
        for neighbor in generate_neighbors_3d(cell_coordinates):
            if neighbor in all_living_cells:
                num_living_neighbors += 1
        return num_living_neighbors

    num_days_to_simulate = 6
    while num_days_to_simulate > 0:
        tomorrows_living_cells = set()
        for living_cell in living_cells:
            for cell in generate_neighbors_3d(living_cell, True):
                num_living_neighbors = count_living_neighbors(living_cells, cell)
                if cell in living_cells:
                    if num_living_neighbors in [2, 3]:
                        tomorrows_living_cells.add(cell)
                else:
                    if num_living_neighbors == 3:
                        tomorrows_living_cells.add(cell)

        living_cells = tomorrows_living_cells
        num_days_to_simulate -= 1

    #print(len(living_cells))

# Part 2
def part_2():

    # Build up the initial set of living cells
    living_cells = set()

    for y in range(len(input_grid)):
        for x in range(len(input_grid[0])):
            if input_grid[y][x] == "#":
                living_cells.add((x, y, 0, 0))

    def generate_neighbors_4d(cell_coordinates, include_self=False):
        offsets = [-1, 0, 1]
        neighbor_offsets = set()
        for x in offsets:
            for y in offsets:
                for z in offsets:
                    for w in offsets:
                        neighbor_offsets.add((x, y, z, w))

        if not include_self:
            neighbor_offsets.remove((0, 0, 0, 0))

        neighbors = []
        for neighbor_offset in neighbor_offsets:
            neighbor_x = cell_coordinates[0] + neighbor_offset[0]
            neighbor_y = cell_coordinates[1] + neighbor_offset[1]
            neighbor_z = cell_coordinates[2] + neighbor_offset[2]
            neighbor_w = cell_coordinates[3] + neighbor_offset[3]
            neighbors.append((neighbor_x, neighbor_y, neighbor_z, neighbor_w))

        return neighbors

    # Copied directly from part 1, but changed generate_neighbors_3d call to
    # generate_neighbors_4d call
    def count_living_neighbors(all_living_cells, cell_coordinates):
        num_living_neighbors = 0
        for neighbor in generate_neighbors_4d(cell_coordinates):
            if neighbor in all_living_cells:
                num_living_neighbors += 1
        return num_living_neighbors

    # Copied directly from part 1, but changed generate_neighbors_3d call to
    # generate_neighbors_4d call
    num_days_to_simulate = 6
    while num_days_to_simulate > 0:
        tomorrows_living_cells = set()
        for living_cell in living_cells:
            for cell in generate_neighbors_4d(living_cell, True):
                num_living_neighbors = count_living_neighbors(living_cells, cell)
                if cell in living_cells:
                    if num_living_neighbors in [2, 3]:
                        tomorrows_living_cells.add(cell)
                else:
                    if num_living_neighbors == 3:
                        tomorrows_living_cells.add(cell)

        living_cells = tomorrows_living_cells
        num_days_to_simulate -= 1
        print("{} days left to simulate".format(num_days_to_simulate))

    print(len(living_cells))

part_2()