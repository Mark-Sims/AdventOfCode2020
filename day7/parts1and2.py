import sys, os
import re

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser

abs_input_filepath = os.path.join(script_dir, 'input.txt')

rules = AoCParser(abs_input_filepath).parse_as_list_of_strings()


def clean_rule(rule_string):
    [left, right] = rule_string.split('contain')

    left = left[:-6] # strip off ' bags '
    contents = re.findall('\d+\s\w+\s\w+', right)

    return (left, contents)

rule_map = {}
reverse_rule_map = {}

for rule in rules:
    (left, contents) = clean_rule(rule)
    rule_map[left] = contents
    for bag_type in contents:
        inner_bag = re.findall('[a-z]+\s[a-z]+', bag_type)[0]
        if inner_bag not in reverse_rule_map:
            reverse_rule_map[inner_bag] = set()

        reverse_rule_map[inner_bag].add(left)


def find_bags_containing(bag):
    outer_bags = set()
    for k, v in rule_map.items():
        for bag_type in v:
            if bag in bag_type:
                outer_bags.add(k)
    return outer_bags

# Part 1
bags_to_search = ['shiny gold']
bags_searched = set()
while len(bags_to_search) > 0:
    bag = bags_to_search.pop()
    try:
        wrapping_bags = reverse_rule_map[bag]
    except:
        wrapping_bags = []
    for wrapping_bag in wrapping_bags:
        if wrapping_bag not in bags_to_search:
            bags_to_search.append(wrapping_bag)
            bags_searched.add(wrapping_bag)

print(len(bags_searched))

# Part 2
def get_num_required_contents_for_bag_type(bag_type):
    num_required_bags = 0
    for required_bag_count_and_type in rule_map[bag_type]:
        required_bag_count = re.findall('^\d', required_bag_count_and_type)[0]
        required_bag_type = re.findall('[a-z]+\s[a-z]+', required_bag_count_and_type)[0]
        num_required_bags += int(required_bag_count) + int(required_bag_count) * get_num_required_contents_for_bag_type(required_bag_type)

    return num_required_bags

print(get_num_required_contents_for_bag_type('shiny gold'))