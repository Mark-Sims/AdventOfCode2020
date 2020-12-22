import sys, os
import re
import operator
from functools import reduce
import math

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser, prod

abs_input_filepath = os.path.join(script_dir, 'input.txt')

ingredients_and_allergens_strings = AoCParser(abs_input_filepath).parse_as_list_of_strings()

# Parse input and build some useful data structures
ingredient_to_potential_allergens = {}
allergens_to_ingredients = {}
allergen_to_list_of_ingredient_lists = {}
ingredient_lists = []
for line in ingredients_and_allergens_strings:
    [ingredients, allergens] = line[:-1].split(" (contains ")
    ingredients = ingredients.split()
    allergens = allergens.split(", ")
    ingredient_lists.append(ingredients)
    for allergen in allergens:
        if allergen in allergen_to_list_of_ingredient_lists:
            allergen_to_list_of_ingredient_lists[allergen].append(ingredients)
        else:
            allergen_to_list_of_ingredient_lists[allergen] = [ingredients]
        for ingredient in ingredients:
            if ingredient in ingredient_to_potential_allergens:
                ingredient_to_potential_allergens[ingredient].add(allergen)
            else:
                ingredient_to_potential_allergens[ingredient] = set([allergen])
    for ingredient in ingredients:
        for allergen in allergens:
            if allergen in allergens_to_ingredients:
                allergens_to_ingredients[allergen].add(ingredient)
            else:
                allergens_to_ingredients[allergen] = set([ingredient])

all_allergens = set(allergens_to_ingredients.keys())
all_ingredients = set(ingredient_to_potential_allergens.keys())
# Part 1
def part_1():
    potential_allergens_assigned_to_ingredients = {}
    for allergen in all_allergens:
        for ingredient in all_ingredients:
            ingredient_in_every_ingredient_list_which_contains_allergen = True
            for ingredient_list in allergen_to_list_of_ingredient_lists[allergen]:
                if ingredient not in ingredient_list:
                    ingredient_in_every_ingredient_list_which_contains_allergen = False
                    break
            if ingredient_in_every_ingredient_list_which_contains_allergen:
                print("{} is contained in every ingredient list with a {} allergen".format(ingredient, allergen))
                if allergen in potential_allergens_assigned_to_ingredients:
                    potential_allergens_assigned_to_ingredients[allergen].add(ingredient)
                else:
                    potential_allergens_assigned_to_ingredients[allergen] = set([ingredient])

    ingredient_assigned_to_allergen = {}
    while len(ingredient_assigned_to_allergen) != len(all_allergens):
        for allergen in all_allergens:
            if len(potential_allergens_assigned_to_ingredients[allergen]) == 1:
                # Assign ingedient to allergen
                ingredient = next(iter(potential_allergens_assigned_to_ingredients[allergen]))
                ingredient_assigned_to_allergen[ingredient] = allergen
                # Now remove that ingredient from consideration for other allergens
                for allergen in potential_allergens_assigned_to_ingredients:
                    if ingredient in potential_allergens_assigned_to_ingredients[allergen]:
                        potential_allergens_assigned_to_ingredients[allergen].remove(ingredient)

    non_allergen_ingredients = []
    for ingredient in all_ingredients:
        if ingredient not in ingredient_assigned_to_allergen:
            non_allergen_ingredients.append(ingredient)

    count = 0    
    for non_allergen in non_allergen_ingredients:
        for ingredient_list in ingredient_lists:
            if non_allergen in ingredient_list:
                count += 1

    print(count)
    return ingredient_assigned_to_allergen
    

dangerous_ingredients_list = part_1()

# Part 2
allergens_and_corresponding_ingredient = []
for ingredient in dangerous_ingredients_list:
    allergens_and_corresponding_ingredient.append((dangerous_ingredients_list[ingredient], ingredient))

allergens_and_corresponding_ingredient.sort()

cannonical_dangerous_ingredients_list = []
for allergen in allergens_and_corresponding_ingredient:
    cannonical_dangerous_ingredients_list.append(allergen[1])

cannonical_dangerous_ingredients_string = ",".join(cannonical_dangerous_ingredients_list)

print(cannonical_dangerous_ingredients_string)