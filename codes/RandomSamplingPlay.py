from MagicCardGame import *
import random
from copy import *
from cards_set import cards
from effects_set import effects

## This random play used to test the balance of the game
## The winning possibility for each player in a random AI play should be 50%

class RandomSamplingPlay:
    def __init__(self, verbose = False):
        self.game = MagicCardGame()
        self.verbose = verbose
        self.winner = -10000

    def initialize(self):
        self.game.initialize()

    def set_state(self, new_game):
        self.game = new_game

    def get_winner(self):
        return self.winner

    def start_game(self):
        if self.verbose:
            self.game.show_state()
        
        while not self.game.is_end():
            self.game.start_turn()
            if self.game.is_end():
                break

            inp = 0
            while inp != 3:
##                input("Enter any key to continue: ")
                if self.verbose:
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
                if self.verbose:
                    print("Action:", inp)
                if inp == 1:
                    card_id = random.choice(self.game.available_play_cards())
                    if self.verbose:
                        print("Playing card:", cards[card_id][0])
                    if cards[card_id][3] is not None:
                        if self.verbose:
                            self.game.show_available_play_card_targets(card_id)
                        target = random.choice(self.game.available_play_card_targets(card_id))
                    else:
                        target = None
                    if self.verbose:
                        print("Target =", target)
                    self.game.play_card(card_id, target = target)
                    if self.game.is_end():
                        break
                elif inp == 2:
                    attacker_position = random.choice(self.game.available_attackers())
                    if self.verbose:
                        print("Attacker: ", attacker_position)
                        self.game.show_available_attacking_targets(attacker_position)
                    target_position = random.choice(self.game.available_attacking_targets(attacker_position))
                    if self.verbose:
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
        if self.verbose:
            self.game.show_state()
            self.game.end_game()
        self.winner = self.game.get_winner()






if __name__ == "__main__":
    n = 100
    while True:
        summ = 0
        for i in range(n):
            play = RandomSamplingPlay()
            play.initialize()
            play.start_game()
            winner = play.get_winner()
            if winner < 0:
                winner = 0.5
            summ += winner
        ave = summ/n
        print("Winner sum = %d" % summ)
        print("Average winner is: %f" % ave)
        n = int(input("n = "))
