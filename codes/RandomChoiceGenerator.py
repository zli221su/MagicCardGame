from MagicCardGame import *
from random import *
import random
from copy import *
from cards_set import cards
from effects_set import effects


class RandomChoiceGenerator:
    def __init__(self, old_game):
        self.game = old_game.get_deep_copy()

    def get_random_play(self):
        random_play_list = []
        available_set = ()
        if len(self.game.available_play_cards()) != 0:
            available_set += (1,)
        if len(self.game.available_attackers()) != 0:
            available_set += (2,)
        if len(available_set) == 2:
            inp = randint(1,2)
        else:
            available_set += (3,)
            inp = available_set[0]
        random_play_list.append(inp)
        if inp == 1:
            card_id = random.choice(self.game.available_play_cards())
            random_play_list.append(card_id)
            if cards[card_id][3] is not None:
                target = random.choice(self.game.available_play_card_targets(card_id))
            else:
                target = None
            random_play_list.append(target)
            self.game.play_card(card_id, target = target)
        elif inp == 2:
            attacker_position = random.choice(self.game.available_attackers())
            random_play_list.append(attacker_position)
            target_position = random.choice(self.game.available_attacking_targets(attacker_position))
            random_play_list.append(target_position)
            self.game.attack(attacker_position, target_position)
        elif inp == 3:
            random_play_list.append(None)
            random_play_list.append(None)
        return self.game, random_play_list




            
