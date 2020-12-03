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
        positional_requirements, self.letter = requirement.split()
        self.first_position, self.second_position = positional_requirements.split('-')
        self.first_position = int(self.first_position)
        self.second_position = int(self.second_position)

    def validate_password_against_policy_requirement(self, password):
        first_position_has_letter = password[self.first_position - 1] == self.letter
        second_position_has_letter = password[self.second_position - 1] == self.letter

        if (first_position_has_letter and second_position_has_letter):
            return False
            
        return first_position_has_letter or second_position_has_letter


count = 0
for policy_password_line in input_list:
    if PasswordPolicy(policy_password_line).validate():
        count += 1

print(count)