import sys, os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser

abs_input_filepath = os.path.join(script_dir, 'input.txt')

adapter_ratings = AoCParser(abs_input_filepath).parse_as_list_of_ints()

# Part 1
adapter_ratings.sort()

cur = 0
cumulative_difference = 0
diff_1 = 0
diff_3 = 0
for index in range(len(adapter_ratings)):
    difference = adapter_ratings[index] - cur
    cumulative_difference += difference
    cur = cumulative_difference
    if difference == 1:
        diff_1 += 1
    if difference == 3:
        diff_3 += 1


cumulative_difference += 3
diff_3 += 1

print(cumulative_difference)
print(diff_1 * diff_3)

# Part 2
adapter_pool = set(adapter_ratings)
memo = {}
last_adapter = adapter_ratings[-1]

def count_adapter_chains(max_adapter_rating):
    if max_adapter_rating in memo:
        return memo[max_adapter_rating]

    if max_adapter_rating == last_adapter:
        memo[max_adapter_rating] = 1
        return 1

    count = 0
    if max_adapter_rating + 1 in adapter_pool:
        count += count_adapter_chains(max_adapter_rating + 1)
    if max_adapter_rating + 2 in adapter_pool:
        count += count_adapter_chains(max_adapter_rating + 2)
    if max_adapter_rating + 3 in adapter_pool:
        count += count_adapter_chains(max_adapter_rating + 3)

    memo[max_adapter_rating] = count
    return count

print(count_adapter_chains(0))

