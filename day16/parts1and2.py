import sys, os
import re
import operator
from functools import reduce

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser, prod

abs_input_filepath = os.path.join(script_dir, 'input.txt')

input = AoCParser(abs_input_filepath).parse_as_list_of_paragraphs()

class Range:
    def __init__(self, range_string):
        [min, max] = range_string.split("-")
        self.min = int(min)
        self.max = int(max)

    def test(self, candidate):
        candidate = int(candidate)
        return candidate >= self.min and candidate <= self.max

    def __repr__(self):
        return "[{}-{}]".format(self.min, self.max)

rule_dict = {}
all_ranges = []
for rule in input[0]:
    [field, ranges] = rule.split(": ")
    ranges = ranges.split(" or ")
    rule_dict[field] = [Range(ranges[0]), Range(ranges[1])]
    all_ranges += rule_dict[field]

# Part 1
invalid_values = []
invalid_tickets = set()
for ticket in input[2][1:]: # Skip the first line of this paragraph which is the "nearby tickets:" label
    values = ticket.split(",")
    for value in values:
        value = int(value)
        found_valid_range = False
        for num_range in all_ranges:
            if num_range.test(value):
                found_valid_range = True
                break # No need to keep checking other ranges, we already know this value falls into a range

        if not found_valid_range:
            invalid_values.append(value)
            invalid_tickets.add(ticket)

print(sum(invalid_values))

# Part 2
class Rule:
    def __init__(self, ranges):
        self.ranges = ranges

    def test(self, candidate):
        for num_range in self.ranges:
            if num_range.test(candidate):
                return True

        return False

    def __repr__(self):
        return " OR ".join([repr(num_range) for num_range in self.ranges])


# Create a dictionary of Rule values rather than a list (of Ranges) values
rule_dict = {k : Rule(v) for k, v in rule_dict.items()}

valid_tickets = input[2][1:]
for invalid_ticket in invalid_tickets:
    valid_tickets.remove(invalid_ticket)

# Convert valid tickets to integer lists, rather than strings
valid_tickets = [[int(value) for value in ticket.split(",")] for ticket in valid_tickets]

# Create a dictionary mapping field_name -> ticket field indices for which all values satisfy this field's rule
field_dict = {}
for field in rule_dict:
    field_dict[field] = list(range(len(rule_dict)))

for field in rule_dict:
    for i in range(len(rule_dict)):
        for ticket in valid_tickets:
            result = rule_dict[field].test(ticket[i])
            if not result:
                #print("Ticket field #{} DOES NOT comply with field '{}'".format(i, field))
                #print("Rule: {} Ticket value: {}".format(rule_dict[field], ticket[i]))
                field_dict[field].remove(i)
                break

assigned_fields = {}

while len(assigned_fields) < len(field_dict):
    # Find which field has only a single ticket field index for which it is valid
    assigned_field = None
    for field in field_dict:
        if len(field_dict[field]) == 1:
            assigned_field = field_dict[field][0]
            assigned_fields[field] = assigned_field

    for field in field_dict:
        try:
            field_dict[field].remove(assigned_field)
        except:
            pass

#print(assigned_fields)

my_ticket_values = [int(val) for val in input[1][1].split(",")]
my_relevant_ticket_values = []
for field in assigned_fields:
    if re.match("^departure", field):
        my_relevant_ticket_values.append(my_ticket_values[assigned_fields[field]])


print(prod(my_relevant_ticket_values))