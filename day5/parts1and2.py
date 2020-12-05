import sys, os
import re

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser

abs_input_filepath = os.path.join(script_dir, 'input.txt')

encoded_boarding_passes = AoCParser(abs_input_filepath).parse_as_list_of_strings()


def decode(min_row, max_row, encoded_row):
    for step in encoded_row:
        #print("min: {}, max: {}, candidates remaining: {}".format(min_row, max_row, max_row - min_row + 1))
        if(step == 'F' or step == 'L'):
            max_row = int((min_row + max_row) / 2)
        elif(step == 'B' or step == 'R'):
            min_row = int((min_row + max_row) / 2) + 1

    if min_row == max_row:
        return min_row

def decode_row(encoded_row):
    return decode(0, 127, encoded_row)

def decode_col(encoded_col):
    return decode(0, 7, encoded_col)

def decode_boarding_pass(encoded_boarding_pass):
    encoded_row = [row_step for row_step in encoded_boarding_pass[0:7]]
    encoded_col = [col_step for col_step in encoded_boarding_pass[7:10]]

    row_pos = decode_row(encoded_row)
    col_pos = decode_col(encoded_col)

    return row_pos, col_pos

max_sid = 0
all_seat_ids = []
for encoded_boarding_pass in encoded_boarding_passes:
    row_pos, col_pos = decode_boarding_pass(encoded_boarding_pass)
    sid = row_pos * 8 + col_pos
    all_seat_ids.append(sid)
    max_sid = max(max_sid, sid)

print(max_sid)

all_seat_ids.sort()
offset = all_seat_ids[0]
for i in range(len(all_seat_ids)):
    if all_seat_ids[i] - (offset + i) != 0:
        print(all_seat_ids[i - 1])
        print(all_seat_ids[i])
        break

a = 5
