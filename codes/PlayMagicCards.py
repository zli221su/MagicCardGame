from MagicCardGame import *
import random
from copy import *
from cards_set import cards
from effects_set import effects



class PlayMagicCard:
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
                self.game.show_state()
                self.game.show_available_play_cards()
                self.game.show_available_attackers()
                available_set = (3,)
                if len(self.game.available_play_cards()) != 0:
                    available_set += (1,)
                if len(self.game.available_attackers()) != 0:
                    available_set += (2,)
                inp = "x"
                while inp not in available_set:
                    inp = int(input("Actions: 1.play 2.attack 3.end turn: "))

                if inp == 1:
                    card_id = "x"
                    while card_id not in tuple(self.game.available_play_cards()):
                        card_id = int(input("Choose a card to play: "))
                    if cards[card_id][3] is not None:
                        self.game.show_available_play_card_targets(card_id)
                        target = "x"
                        while target not in self.game.available_play_card_targets(card_id):
                            target = int(input("Choose a target: "))
                    else:
                        target = None
                    self.game.play_card(card_id, target = target)
                    if self.game.is_end():
                        break
                elif inp == 2:
                    attacker_position = "x"
                    while attacker_position not in self.game.available_attackers():
                        attacker_position = int(input("Choose an attacker minion: "))
                    self.game.show_available_attacking_targets(attacker_position)
                    target_position = "x"
                    while target_position not in self.game.available_attacking_targets(attacker_position):
                        target_position = int(input("Choose a target: "))
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

    play = PlayMagicCard()

    play.initialize()
    play.start_game()
    
