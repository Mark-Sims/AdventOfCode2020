import sys, os
import re
import operator
from functools import reduce

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser, prod

abs_input_filepath = os.path.join(script_dir, 'input.txt')

equations = AoCParser(abs_input_filepath).parse_as_list_of_strings()

# Part 1
def find_end_paren_index(equation, position):
    paren_depth = 0
    start = position
    while position < len(equation):
        if equation[position] == '(':
            paren_depth += 1
        elif equation[position] == ")":
            paren_depth -= 1

        position += 1
        if paren_depth == 0:
            return position

def part_1():

    def evaluate(equation):
        i = 0
        term_1 = 0
        operator = "+"
        while i < len(equation):
            operator_term = re.findall("^(\+|\*)", equation[i])
            digit_term = re.findall("^[0-9]+", equation[i:])
            if equation[i] == '(':
                end = find_end_paren_index(equation, i)
                param_eval = evaluate(equation[i + 1:end - 1])
                if operator == "+":
                    term_1 += param_eval
                elif operator == "*":
                    term_1 *= param_eval
                i = end

            if digit_term:
                i += len(digit_term[0])
                if operator == "+":
                    term_1 += int(digit_term[0])
                elif operator == "*":
                    term_1 *= int(digit_term[0])
            if operator_term:
                i += 1
                operator = operator_term[0]

        return term_1

    answers = []
    for equation in equations:
        answers.append(evaluate(equation.replace(" ", "")))

    #print(sum(answers))

# Part 2

def evaluate_additions(equation):
    addition = re.search("[0-9]+\+[0-9]+", equation)
    while addition:
        start = addition.start()
        end = addition.end()
        [first, second]  = equation[start:end].split("+")
        sub = int(first) + int(second)
        equation = equation[:start] + str(sub) + equation[end:]

        # Next iteration
        addition = re.search("[0-9]+\+[0-9]+", equation)

    return equation

def evaluate_multiplications(equation):
    multiplication = re.search("[0-9]+\*[0-9]+", equation)
    while multiplication:
        start = multiplication.start()
        end = multiplication.end()
        [first, second]  = equation[start:end].split("*")
        sub = int(first) * int(second)
        equation = equation[:start] + str(sub) + equation[end:]

        # Next iteration
        multiplication = re.search("[0-9]+\*[0-9]+", equation)

    return equation

def remove_single_number_parens(equation):
    unnecessary_paren = re.search("\([0-9]+\)", equation)
    while unnecessary_paren:
        start = unnecessary_paren.start()
        end = unnecessary_paren.end()
        sub = equation[start + 1:end - 1]
        equation = equation[:start] + sub + equation[end:]
        unnecessary_paren = re.search("\([0-9]+\)", equation)

    return equation

def evaluate(equation):
    open_paren = re.search("\(", equation)
    while open_paren:
        start = open_paren.start()
        end = find_end_paren_index(equation, start)
        equation = equation[:start] + evaluate(equation[start + 1:end - 1]) + equation[end:]
        open_paren = re.search("\(", equation)
    
    equation = evaluate_additions(equation)
    equation = evaluate_multiplications(equation)

    return equation


answers = []
for equation in equations:
    equation = equation.replace(" ", "")
    answers.append(int(evaluate(equation)))

print(sum(answers))

