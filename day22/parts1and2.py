import sys, os
import re
import operator
from functools import reduce
import math
from collections import deque

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
sys.path.append(os.path.join(script_dir, '..', 'common'))
from common import AoCParser, prod

abs_input_filepath = os.path.join(script_dir, 'input.txt')

players_hands = AoCParser(abs_input_filepath).parse_as_list_of_paragraphs()

player_1_hand = deque([int(card) for card in players_hands[0][1:]])
player_2_hand = deque([int(card) for card in players_hands[1][1:]])

def play_combat():
    while len(player_1_hand) > 0 and len(player_2_hand) > 0:
        player_1_card = player_1_hand.popleft()
        player_2_card = player_2_hand.popleft()

        if player_1_card > player_2_card:
            player_1_hand.append(player_1_card)
            player_1_hand.append(player_2_card)
        else:
            player_2_hand.append(player_2_card)
            player_2_hand.append(player_1_card)

    if len(player_1_hand) > 0:
        return player_1_hand
    else:
        return player_2_hand

def calculate_score(hand):
    score = 0
    for card_index in range(len(hand)):
        score += (len(hand) - card_index) * hand[card_index]

    return score

#winning_hand = play_combat()
#print(calculate_score(winning_hand))

# Part 2
# True = Player 1 Wins
# False = Player 2 Wins
def play_recursive_combat(player_1_deck, player_2_deck):
    if len(player_1_deck) == 0:
        return False
    elif len(player_2_deck) == 0:
        return True

    decks_seen = set()

    while len(player_1_deck) > 0 and len(player_2_deck) > 0:

        hashable_decks = ",".join([str(x) for x in player_1_deck]) + "|" + ",".join([str(x) for x in player_2_deck])
        if hashable_decks in decks_seen:
            return True
        decks_seen.add(hashable_decks)

        player_1_card = player_1_deck.popleft()
        player_2_card = player_2_deck.popleft()

        winner = None

        if len(player_1_deck) >= player_1_card and len(player_2_deck) >= player_2_card:
            winner = play_recursive_combat(
                deque(list(player_1_deck)[0:player_1_card]),
                deque(list(player_2_deck)[0:player_2_card])
            )
        elif player_1_card > player_2_card:
            winner = True
        else:
            winner = False

        if winner:
            player_1_deck.append(player_1_card)
            player_1_deck.append(player_2_card)
        else:
            player_2_deck.append(player_2_card)
            player_2_deck.append(player_1_card)

    if len(player_1_deck) > 0:
        return True
    else:
        return False

play_recursive_combat(player_1_hand, player_2_hand)

if len(player_1_hand) > 0:
    print(calculate_score(player_1_hand))
else:
    print(calculate_score(player_2_hand))