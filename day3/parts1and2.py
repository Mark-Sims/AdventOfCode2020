import sys, os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))

abs_input_filepath = os.path.join(script_dir, 'input.txt')

from common import AoCParser

map = AoCParser(abs_input_filepath).parse_as_2d_list()

map_width = len(map[0])

def count_trees_on_slope(step_x, step_y):
    tree_counter = 0
    pos_x = 0
    pos_y = 0
    while pos_y < len(map):
        if pos_x >= map_width:
            pos_x = pos_x % map_width

        if map[pos_y][pos_x] == '#':
            tree_counter += 1

        pos_x = pos_x + step_x
        pos_y = pos_y + step_y

    return tree_counter

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
total_trees = []
for slope in slopes:
    step_x, step_y = slope
    total_trees.append(count_trees_on_slope(step_x, step_y))
    
multiplied_total = 1
for trees in total_trees:
    multiplied_total *= trees

print(multiplied_total)