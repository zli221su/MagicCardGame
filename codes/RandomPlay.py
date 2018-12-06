from MagicCardGame import *
import random
from copy import *
from cards_set import cards
from effects_set import effects



class RandomPlayMagicCard:
    def __init__(self):
        self.game = MagicCardGame()

    def initialize(self):
        self.game.initialize()

    def start_game(self):
        self.game.show_state()
        
        while not self.game.is_end():
            self.game.start_turn()
            if self.game.is_end():
                break

            inp = 0
            while inp != 3:
                input("Enter any key to continue: ")
                self.game.show_state()
                self.game.show_available_play_cards()
                self.game.show_available_attackers()
                available_set = ()
                if len(self.game.available_play_cards()) != 0:
                    available_set += (1,)
                if len(self.game.available_attackers()) != 0:
                    available_set += (2,)
                available_set += (3,)
                inp = available_set[0]
                print("Action:", inp)
                if inp == 1:
                    card_id = random.choice(self.game.available_play_cards())
                    print("Playing card:", cards[card_id][0])
                    if cards[card_id][3] is not None:
                        self.game.show_available_play_card_targets(card_id)
                        target = random.choice(self.game.available_play_card_targets(card_id))
                    else:
                        target = None
                    print("Target =", target)
                    self.game.play_card(card_id, target = target)
                    if self.game.is_end():
                        break
                elif inp == 2:
                    attacker_position = random.choice(self.game.available_attackers())
                    print("Attacker: ", attacker_position)
                    self.game.show_available_attacking_targets(attacker_position)
                    target_position = random.choice(self.game.available_attacking_targets(attacker_position))
                    print("Attacked target:", target_position)
                    self.game.attack(attacker_position, target_position)
                    if self.game.is_end():
                        break
                elif inp == 3:
                    break
                else:
                    print("Invalid option!")
            if self.game.is_end():
                break
            self.game.end_turn()
        self.game.show_state()
        self.game.end_game()






if __name__ == "__main__":

    play = RandomPlayMagicCard()

    play.initialize()
    play.start_game()
    
