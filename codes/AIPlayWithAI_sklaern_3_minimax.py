from MagicCardGame import *
from MinimaxPlayWithRandomSampling import *
from RandomChoiceGenerator import *
import random
from copy import *
from cards_set import cards
from effects_set import effects

from sklearn import svm


class SklearnAI:
    def __init__(self, game, clf):
        self.game = game.get_deep_copy()
        self.temp_game = game.get_deep_copy()
        self.clf = clf
        self.max_utility = -10
        self.choice = ()
        self.player = self.game.get_current_player()

    def do_scoring(self):
        training_X = list(self.temp_game.get_state_tuple_without_opponent(self.player))        
        u = self.clf.predict([training_X])
        if abs(self.player - u) < abs(self.player - self.max_utility): ## if this utility is closer to this player(more possible to win), return true
            self.max_utility = u
            return True
        else:
            return False

    def renew_game(self):
        self.temp_game = self.game.get_deep_copy()


    def get_best_choice(self):
        ##search plays
        for card_id in self.game.available_play_cards():
            if self.game.needs_target(card_id):
                for target_position in self.game.available_play_card_targets(card_id):
                    self.renew_game()
                    self.temp_game.play_card(card_id, target = target_position)
                    if self.do_scoring():
                        self.choice = (1, card_id, target_position)
            else: ## target not needed
                self.renew_game()
                self.temp_game.play_card(card_id)
                if self.do_scoring():
                    self.choice = (1, card_id, None)
        ##search actions
        for attacker_position in self.game.available_attackers():
            for target_position in self.game.available_attacking_targets(attacker_position):
                self.renew_game()
                self.temp_game.attack(attacker_position, target_position)
                if self.do_scoring():
                    self.choice = (2, attacker_position, target_position)
        ##end turn
        self.renew_game()
        self.temp_game.end_turn()
        self.temp_game.start_turn()
        if len(self.choice) < 1:
            self.choice = (3,)
        return self.choice, self.max_utility


class WildPlay:
    def __init__(self, AI = ("random", "random"), AI_iteration = (0, 0)):
        self.game = None
        self.turn = 0
        self.AI = AI
        self.clf = None
        self.AI_iteration = AI_iteration

    def initialize(self):
        if self.AI[0] == "sklearn" or self.AI[1] == "sklearn":
            print("importing training_set_X")
            from training_set_X_10000_2_test import X as training_set_X
            from training_set_Y_10000_2_test import Y as training_set_Y
            self.clf = svm.SVR(kernel = 'linear')
            print("fitting sklearn")
            self.clf.fit(training_set_X, training_set_Y)

    def reset_game(self):
        self.game = MagicCardGame()
        self.game.initialize()
        self.turn = 0

    def get_current_choice(self):
        if self.AI[self.game.get_current_player()] == "random":
            ## random choice
            available_set = ()
            if len(self.game.available_attackers()) != 0:
                available_set += (2,)
            elif len(self.game.available_play_cards()) != 0:
                available_set += (1,)
            else:
                available_set += (3,)
            
            inp = available_set[0]
            if inp == 1:
                card_id = random.choice(self.game.available_play_cards())
                available_set += (card_id,)
                target = None
                if cards[card_id][3] is not None:
                    target = random.choice(self.game.available_play_card_targets(card_id))
                available_set += (target,)
            elif inp == 2:
                attacker_position = random.choice(self.game.available_attackers())
                target_position = random.choice(self.game.available_attacking_targets(attacker_position))
                available_set += (attacker_position, target_position,)
            elif inp == 3:
                available_set += (None, None)
            else:
                print("Invalid option!")
            return available_set, None
        
        elif self.AI[self.game.get_current_player()] == "minimax":
            ## minimax choice
            minimax = MinimaxWithSampling(self.game)
            current_choice = minimax.search()
            win_rate = minimax.max_utility
            return current_choice, win_rate
        
        elif self.AI_iteration[self.game.get_current_player()] > 0:
            ## sklearn AI choice
            return SklearnAI(self.game, self.clf).get_best_choice()
        else:
            raise Exception ("Invalid AI!")
        

    def play_game(self, verbose = False):
        if verbose:
            self.game.show_state()
        while not self.game.is_end():
            self.turn += 1
            self.game.start_turn()
            if self.game.is_end():
                break
            inp = 0
            while inp != 3:
##                input("Enter any key to continue: ")
                if verbose:
                    self.game.show_state()
                    self.game.show_available_play_cards()
                    self.game.show_available_attackers()
                current_choice, win_rate = self.get_current_choice()
                inp = current_choice[0]
                if verbose:
                    print("Action:", inp)
                if inp == 1:
                    card_id = current_choice[1]
                    if verbose:
                        print("Playing card:", cards[card_id][0])
                    target = current_choice[2]
                    if verbose:
                        print("Target =", target)
                    self.game.play_card(card_id, target = target)
                    if self.game.is_end():
                        break
                elif inp == 2:
                    attacker_position = current_choice[1]
                    if verbose:
                        print("Attacker: ", attacker_position)
                        self.game.show_available_attacking_targets(attacker_position)
                    target_position = current_choice[2]
                    if verbose:
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
        if verbose:
            self.game.show_state()
            self.game.end_game()
        print(" run_turns = %d, Winner is player %s!" % (self.turn, self.game.get_winner()))


if __name__ == "__main__":

    AI = ("sklearn", "minimax")
    AI_iteration = (3, 0)

    print("AI = %s, AI_iteration = %s" %(AI, AI_iteration))

    runs = 500
    
    play = WildPlay(AI = AI, AI_iteration = AI_iteration)
    
    play.initialize()
    count = 0
    for i in range(runs):
        count += 1
        print("Play = %d," % count, end = "  ")
        play.reset_game()
        play.play_game()
    

