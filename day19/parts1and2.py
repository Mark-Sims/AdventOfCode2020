import sys, os
import re
import operator
from functools import reduce

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser, prod

abs_input_filepath = os.path.join(script_dir, 'input.txt')

[rules, messages] = AoCParser(abs_input_filepath).parse_as_list_of_paragraphs()

# Part 1

rule_bank = {}

#class Rule:
#    def __init__(self, rule_description):
#        [self.rule_num, rule_reqs] = rule_description.split(": ")
#        self.disjunctive_terms = []
#        self.val = None
#        if re.match('"[a-z]"', rule_reqs):
#            self.val = rule_reqs[1]
#            print("Rule {} is a simple rule with val: {}".format(self.rule_num, rule_reqs[1]))
#        elif "|" in rule_reqs:
#            print("Rule {} is a disjunctive rule".format(self.rule_num))
#            [term_1, term_2] = rule_reqs.split(" | ")
#            if " " in term_1:
#                self.disjunctive_terms.append(term_1.split())
#            else:
#                self.disjunctive_terms.append([term_1])
#            if " " in term_2:
#                self.disjunctive_terms.append(term_2.split())
#            else:
#                self.disjunctive_terms.append([term_2])
#        else:
#            print("Rule {} is a conjunctive rule".format(self.rule_num))
#            self.disjunctive_terms.append(rule_reqs.split())
#
#    def __repr__(self):
#        if self.val:
#            return self.val
#        if len(self.disjunctive_terms) == 1:
#            return str(self.disjunctive_terms[0])
#        print(len(self.disjunctive_terms))
#        return "{} | {}".format(self.disjunctive_terms[0], self.disjunctive_terms[1])
#
#    def __str__(self):
#        return "test"

rule_consumption = {}

class Rule:
    def __init__(self, reqs):
        self.or_rules = []
        self.and_rules = []
        self.val = None
        self.resolvable_rule = None
        if "|" in reqs:
            self.or_rules = [Rule(term) for term in reqs.split(" | ")]
        elif " " in reqs:
            self.and_rules = [Rule(term) for term in reqs.split()]
        elif '"' in reqs:
            self.val = reqs[1] # Strip off the quotes
        else:
            self.resolvable_rule = reqs

    def validate_string(self, string):
        if len(string) == 0:
            return True
        for r in self.or_rules:
            if r.validate_string(string):
                return True
        if len(self.or_rules) > 0:
            return False

        for rule_num in range(len(self.and_rules)):
            r = self.and_rules[rule_num]
            if not r.validate_string(string[rule_num:]):
                return False
        if len(self.and_rules) > 0:
            return True

        if self.val:
            if string[0] == self.val:
                return True

        if self.resolvable_rule:
            return rule_bank[self.resolvable_rule].validate_string(string)
        
        return False

# First, identify the simple, rules
#for rule_str in rules:
#    if '"' in rule_str:
#        [rule_num, rule_reqs] = rule_str.split(": ")
#        rule_bank[rule_num] = Rule(rule_reqs)


for rule_str in rules:
    [rule_num, rule_reqs] = rule_str.split(": ")
    rule_bank[rule_num] = Rule(rule_reqs)

a = 5

#for rule_num, rule in rule_bank.items():
#    if rule.val:
#        rule_consumption[rule_num] = 1
#
#
#def get_consumption(rule_num):
#    if rule_num in rule_consumption:
#        return rule_consumption[rule_num]
#
#    rule = rule_bank[rule_num]
#    if len(rule.or_rules) > 0:
#        a = [get_consumption(r) for r in rule.or_rules]
#        for i in a:
#            if a[0] != i:
#                print(a)
#                raise
#        rule_consumption[rule_num] = a[0]
#
#    consumption = 0    
#    if len(rule.and_rules) > 0:
#        for r in rule.and_rules:
#            consumption += get_consumption(r)
#
#
#for rule_num, rule in rule_bank.items():
#    get_consumption(rule_num)


#print(rule_bank["2"].validate_string("aa"))
#print(rule_bank["2"].validate_string("ab"))
#print(rule_bank["2"].validate_string("ba"))
#print(rule_bank["2"].validate_string("bb"))
#
#print(rule_bank["3"].validate_string("aa"))
#print(rule_bank["3"].validate_string("ab"))
#print(rule_bank["3"].validate_string("ba"))
#print(rule_bank["3"].validate_string("bb"))
# Part 1


#print(rule_bank["0"].validate_string("aaaabb"))
#print(rule_bank["8"].validate_string("abcd"))
#print(rule_bank["1"].validate_string("aaab"))

# Part 1
def part_1():
    def build_all_strings(rule):
        if rule.resolvable_rule:
            return build_all_strings(rule_bank[rule.resolvable_rule])
        if rule.val:
            return [rule.val]

        if len(rule.or_rules) > 0:
            lst = []
            for r in rule.or_rules:
                a = build_all_strings(r)
                lst.append(a)

            return [item for sublist in lst for item in sublist]


        if len(rule.and_rules) > 0:
            a = build_all_strings(rule.and_rules[0])
            if(len(rule.and_rules) == 1):
                return a

            new_ret = a.copy()

            for r in rule.and_rules[1:]:
                new_ret = []
                b = build_all_strings(r)
                if(len(a) >= len(b)):
                    for partial_a in a:
                        for partial_b in b:
                            new = partial_a + partial_b
                            new_ret.append(new)
                else:
                    for pratial_b in b:
                        for partial_a in a:
                            new = partial_a + pratial_b
                            new_ret.append(new)

                a = new_ret

            return new_ret


    zero_rule_strings = build_all_strings(rule_bank["0"])

    c = 0
    for i in messages:
        if i in zero_rule_strings:
            c += 1

    print(c)

validation_string = ""
# Part 2
def part_2():
    global validation_string
    def build_all_strings(rule):
        if rule.resolvable_rule:
            return build_all_strings(rule_bank[rule.resolvable_rule])
        if rule.val:
            return [rule.val]

        if len(rule.or_rules) > 0:
            lst = []
            for r in rule.or_rules:
                a = build_all_strings(r)
                lst.append(a)

            return [item for sublist in lst for item in sublist]


        if len(rule.and_rules) > 0:
            a = build_all_strings(rule.and_rules[0])
            if(len(rule.and_rules) == 1):
                return a

            new_ret = a.copy()

            for r in rule.and_rules[1:]:
                new_ret = []
                b = build_all_strings(r)
                if(len(a) >= len(b)):
                    for partial_a in a:
                        for partial_b in b:
                            new = partial_a + partial_b
                            new_ret.append(new)
                else:
                    for pratial_b in b:
                        for partial_a in a:
                            new = partial_a + pratial_b
                            new_ret.append(new)

                a = new_ret
            return new_ret

    rule_expansions = {}
    for rule in rule_bank:
        # Rule 0 expands to rules 8 and 11
        # Rules 8 and 11 are both recursively defined, so they would expand to be infinitely long
        if rule == "0" or rule == "8" or rule == "11":
            continue
        expansions = set(build_all_strings(rule_bank[rule]))
        rule_expansions[rule] = expansions


    # 8: 42 | 42 8
    # Notice that rule 8 is just repeated instances of rule 42

    # 11: 42 31 | 42 11 31
    # Notice that rule 11 is repeated instances of rule 42 followed by the same number of instances of rule 31

    validation_string = ""

    def validate_message(msg, moved_on_from_11s, found_one_8, found_one_11):
        global validation_string
        if msg == "":
            return found_one_8 and found_one_11

        if msg[:8] in rule_expansions["42"] and msg[-8:] in rule_expansions["31"] and not moved_on_from_11s:
            #print("{} matches rule 11".format(msg))
            validation_string = "11, " + validation_string
            return validate_message(msg[8:-8], False, False, True)

        if msg[:8] in rule_expansions["42"]:
            #print("{} matches rule 8".format(msg))
            validation_string = "8, " + validation_string
            return validate_message(msg[8:], True, True, found_one_11)
        
        return False


    #validate_message('bbabbaabaabaaaababbbbabaabbaabab', False)

    counter = 0
    for message in messages:
        validation_string = ""
        if validate_message(message, False, False, False):
            print(validation_string)
            #print("Overall valid message: {}".format(message))
            counter += 1
        else:
            print("Invalid message: {}     Validation string: {}".format(message, validation_string))

    print(counter)

part_2()

# 326 is too high - forgot to consider that you need at least one 8
# 25 is wrong
# 150 is too low
# 170 is wrong
# 321 is wrong (right answer for someone else) - forgot to consider that you need at least one 11
# 301 <- That's it!

