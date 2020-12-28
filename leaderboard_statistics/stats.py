import sys, os
import json

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
abs_input_filepath = os.path.join(script_dir, '190418.json')
abs_input_filepath = os.path.join(script_dir, '2020.12.22_16.13.15_190418.json')
abs_input_filepath = os.path.join(script_dir, '2020.12.24_06.17.49_190418.json')
abs_input_filepath = os.path.join(script_dir, '2020.12.27_22.13.19_190418.json')

with open(abs_input_filepath, 'r', encoding='utf-8') as fh:
    data = json.load(fh)

member_name_to_id = {}
completion_order = {}
member_dict = data['members']
for member_id in member_dict:
    member_name = member_dict[member_id]['name']

    if member_name is None:
        member_name = "anonymous user #{}".format(member_id)
    member_name_to_id[member_name] = member_id

    if member_name == 'Mark-Sims':
        a = 5
        pass

    member_completion_dict = member_dict[member_id]["completion_day_level"]
    for day in member_completion_dict:
        for part in member_completion_dict[day]:
            star_code_key = "{}-{}".format(day, part)
            if star_code_key not in completion_order:
                completion_order[star_code_key] = []
            completion_order[star_code_key].append((member_completion_dict[day][part]['get_star_ts'], member_name))

def get_stats_for_user(user, day=None):
    total = 0
    for star in completion_order:
        completion_order[star].sort()
        completion_rank = [i for i, v in enumerate(completion_order[star]) if v[1] == user][0]
        total_completions_for_star = len(completion_order[star])
        total_leaderboard_count = len(member_name_to_id)
        star_points = total_leaderboard_count - completion_rank

        if day is None or (star in ["{}-1".format(day), "{}-2".format(day)]):
            print("For star {}, you were {}/{} out of a total {} members on this leaderboard.".format(star, completion_rank, total_completions_for_star, total_leaderboard_count))
            if star != "1-1" and star != "1-2":
                print("This star earned you {} points!".format(star_points))

        # Exclude day 1 for scoring purposes:
        if star != "1-1" and star != "1-2":
            total += star_points
    
    print("Total score for {}: {} points!".format(user, total))

get_stats_for_user('Mark-Sims', 17)
get_stats_for_user('Mark-Sims', 18)
get_stats_for_user('Mark-Sims', 19)
get_stats_for_user('Mark-Sims', 20)
get_stats_for_user('Mark-Sims', 21)
get_stats_for_user('Mark-Sims', 22)
get_stats_for_user('Mark-Sims', 23)
get_stats_for_user('Mark-Sims', 24)
get_stats_for_user('Mark-Sims', 25)
    