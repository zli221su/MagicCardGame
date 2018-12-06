from MagicCardGame import *
import random
from copy import *
from cards_set import cards
from effects_set import effects
from RandomSamplingFromState import *






## AI player == player 0
















## This class can read in a state and do minimax search based on sampling
## Finally it can return the best choice for currentPlayer
class MinimaxWithSampling:    
    def __init__(self, input_game, X = None, Y = None, training_count = [0]):
        self.game =input_game
        self.temp_game = None
        self.max_utility = -10
        self.result = ()
        self.player = self.game.get_current_player()
        self.X = X
        self.Y = Y
        self.training_count = training_count

    def renew_temp_game(self):
        self.temp_game = self.game.get_deep_copy()

    def do_random_sampling(self):
        if self.X is not None:
            training_X = list(self.temp_game.get_state_tuple_without_opponent(self.player))
            self.X.write(str(training_X))
            self.X.write(",\n")
        
        u = RandomSamplingFromState(self.temp_game).do_sampling()
        if self.Y is not None:
            self.Y.write(str(u))
            self.Y.write(",\n")
            self.training_count[0] += 1

        
##        print("u = %s " % u, end = "")
        if abs(self.player - u) < abs(self.player - self.max_utility): ## if this utility is closer to this player(more possible to win), return true
            self.max_utility = u
##            print("self.max_utility = %s" % self.max_utility)
            return True
        else:
            return False

    def search(self):
##        print("run ", end = "")
        ##search plays
        for card_id in self.game.available_play_cards():
            if self.game.needs_target(card_id):
                for target_position in self.game.available_play_card_targets(card_id):
                    self.renew_temp_game()
                    self.temp_game.play_card(card_id, target = target_position)
                    if self.do_random_sampling():
                        self.result = (1, card_id, target_position)
            else: ## target not needed
                self.renew_temp_game()
                self.temp_game.play_card(card_id)
                if self.do_random_sampling():
                    self.result = (1, card_id, None)

        ##search actions
        for attacker_position in self.game.available_attackers():
            for target_position in self.game.available_attacking_targets(attacker_position):
                self.renew_temp_game()
                self.temp_game.attack(attacker_position, target_position)
                if self.do_random_sampling():
                    self.result = (2, attacker_position, target_position)

        ##end turn
        self.renew_temp_game()
        self.temp_game.end_turn()
        self.temp_game.start_turn()
        if self.do_random_sampling():
            self.result = (3,)
        return self.result
    
class PlayMinimaxSamplingWithRandom:
    def __init__(self):
        self.game = MagicCardGame()

    def play(self, verbose = False):
        self.game.initialize()
        if verbose:
            self.game.show_state()

        r = 0
        while not self.game.is_end():
            r += 1
            self.game.start_turn()
            if self.game.is_end():
                break
            inp = -10
            while inp != 3:
                if verbose:
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

                if self.game.get_current_player() == 0: ## use minimax for player 0
                    minimax_result = MinimaxWithSampling(self.game).search()
                    inp = minimax_result[0]
                else: ## use random for player 1
                    inp = available_set[0]
                if verbose:
                    print("Action:", inp)
                if inp == 1:
                    if self.game.get_current_player() == 0: ## use minimax for player 0
                        card_id = minimax_result[1]
                    else: ## use random for player 1
                        card_id = random.choice(self.game.available_play_cards())
                    if verbose:
                        print("Playing card:", cards[card_id][0])
                    if cards[card_id][3] is not None:
                        if verbose:
                            self.game.show_available_play_card_targets(card_id)
                        if self.game.get_current_player() == 0: ## use minimax for player 0
                            target = minimax_result[2]
                        else: ## use random for player 1
                            target = random.choice(self.game.available_play_card_targets(card_id))
                    else:
                        target = None
                    if verbose:
                        print("Target =", target)
                    self.game.play_card(card_id, target = target)
                    if self.game.is_end():
                        break
                elif inp == 2:
                    if self.game.get_current_player() == 0: ## use minimax for player 0
                        attacker_position = minimax_result[1]
                    else: ## use random for player 1
                        attacker_position = random.choice(self.game.available_attackers())
                    if verbose:
                        print("Attacker: ", attacker_position)
                        self.game.show_available_attacking_targets(attacker_position)
                    if self.game.get_current_player() == 0: ## use minimax for player 0
                        target_position = minimax_result[2]
                    else: ## use random for player 1
                        target_position = random.choice(self.game.available_attacking_targets(attacker_position))
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
        print("round = %s" % r, end = "  ")
        return self.game.get_winner()

class TestMinimaxWithSampling():
    def __init__(self, run_times = 500):
        self.play_game = None
        self.winner = None
        self.run_times = run_times

    def initialize(self):
        self.play_game = PlayMinimaxSamplingWithRandom()

    def run(self):
        summ = 0
        for i in range(self.run_times):
            self.initialize()
            winner = self.play_game.play()
            print("run %d,winner is %s" %(i, winner))
            summ += winner
        ave = summ / self.run_times
        print("Sum = %d" % summ)
        print("Ave = %f" % ave)
        print("-----------------------------------------------------------------------------------")



if __name__ == "__main__":

    test = TestMinimaxWithSampling()
    test.run()





















        
