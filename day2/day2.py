import os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
abs_input_filepath = os.path.join(script_dir, 'input.txt')

input_list = []

with open(abs_input_filepath, 'r') as inputfp:
    line = inputfp.readline()
    while(line):
        input_list.append(line)
        line = inputfp.readline()

class PasswordPolicy:
    def __init__(self, line):
        policy_and_password = line.split(':')
        self.policy = PolicyRequirement(policy_and_password[0].strip())
        self.password = policy_and_password[1].strip()

    def validate(self):
        return self.policy.validate_password_against_policy_requirement(self.password)
        

class PolicyRequirement:
    def __init__(self, requirement):
        length_requirement, self.letter = requirement.split()
        self.min_occurrences, self.max_occurrences = length_requirement.split('-')
        self.min_occurrences = int(self.min_occurrences)
        self.max_occurrences = int(self.max_occurrences)

    def count_occurrences_of_letter(letter, string):
        count = 0
        for i in string:
            if i == letter:
                count += 1

        return count

    def validate_password_against_policy_requirement(self, password):
        count = PolicyRequirement.count_occurrences_of_letter(self.letter, password)
        if count > self.max_occurrences or count < self.min_occurrences:
            return False

        return True


count = 0
for policy_password_line in input_list:
    if PasswordPolicy(policy_password_line).validate():
        count += 1

print(count)