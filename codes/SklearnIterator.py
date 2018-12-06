from MagicCardGame import *
from MinimaxPlayWithRandomSampling import *
from RandomChoiceGenerator import *
import random
from copy import *
from cards_set import cards
from effects_set import effects

from sklearn import svm


class SklearnAI:
    def __init__(self, game, clf, X, Y):
        self.game = game.get_deep_copy()
        self.temp_game = game.get_deep_copy()
        self.clf = clf
        self.max_utility = -10
        self.choice = ()
        self.player = self.game.get_current_player()
        self.X = X
        self.Y = Y

    def do_scoring(self):
        training_X = list(self.temp_game.get_state_tuple())
        self.X.write(str(training_X))
        self.X.write(",\n")
        
        u = self.clf.predict(training_X)
        self.Y.write(str(u))
        self.Y.write(",\n")
        
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
        if self.do_scoring():
            self.choice = (3,)
        return self.choice, self.max_utility



class SklearnIterator:
    def __init__(self, AI = "minimax", AI_iteration = 0):
        self.game = None
        self.X = None # X is the state
        self.Y = None # Y is the play choice
        self.AI = AI
        self.clf = None
        self.AI_iteration = AI_iteration

    def initialize(self):
        if self.AI == "sklearn":
            print("importing training_set_X")
            from training_set_X0 import X as training_set_X
            from training_set_Y0 import Y as training_set_Y
            self.clf = svm.SVR(kernel = 'linear')
            print("fitting sklearn")
            self.clf.fit(training_set_X, training_set_Y)
        self.X = open("C:\\Users\\Zhi Li\\Desktop\\CIS 667 Introduction to AI\\Project\\codes\\gaming part\\20181122 game with coin\\training_data\\training_set_X 50 %d.py" % AI_iteration, "w+")
        self.Y = open("C:\\Users\\Zhi Li\\Desktop\\CIS 667 Introduction to AI\\Project\\codes\\gaming part\\20181122 game with coin\\training_data\\training_set_Y 50 %d.py" % AI_iteration, "w+")
        self.X.write("X = [\n")
        self.Y.write("Y = [\n")

    def reset_game(self):
        self.game = MagicCardGame()
        self.game.initialize()

    def get_current_choice(self):
        lst = [0] * (Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 4 + 3 + 1)
        ##           hand0(134),                    target0(14),  battlefield0(7),battlefield_target0(7)  hero0,h1,h1, end_turn
        if self.AI == "minimax":
            minimax = MinimaxWithSampling(self.game, self.X, self.Y)
            current_choice = minimax.search()
            win_rate = minimax.max_utility
            return current_choice, win_rate
        
        elif self.AI_iteration > 0:
            return SklearnAI(self.game, self.clf, self.X, self.Y).get_best_choice()
        else:
            raise Exception ("Invalid AI!")

        

    def play_game(self, verbose = False):
        if verbose:
            self.game.show_state()
        while not self.game.is_end():
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
                    if cards[card_id][3] is not None:
                        if verbose:
                            self.game.show_available_play_card_targets(card_id)
                        target = current_choice[2]
                    else:
                        target = None
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
        print("Winner is player %s!" % self.game.get_winner())




        
        

    def end_game(self):
        self.X.write("\n]")
        self.Y.write("\n]")
        self.X.close()
        self.Y.close()




if __name__ == "__main__":

    AI_iteration = 0

    plays = 50
    if AI_iteration == 0:
        play = SklearnIterator(AI = "minimax", AI_iteration = 0)
    elif AI_iteration > 0:
        play = SklearnIterator(AI = "sklearn", AI_iteration = AI_iteration)
    else:
        raise Exception("Invalid AI_iteration = %s" % AI_iteration)
    play.initialize()
    count = 0
    for i in range(plays):
        count += 1
        print("Play = %d" % count, end = "  ")
        play.reset_game()
        play.play_game()
    play.end_game()
    

