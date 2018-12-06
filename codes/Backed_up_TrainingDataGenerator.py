from MagicCardGame import *
from MinimaxPlayWithRandomSampling import *
from RandomChoiceGenerator import *
import random
from copy import *
from cards_set import cards
from effects_set import effects

from sklearn import svm

##print("importing training_set_X")
##from training_set_X import X as training_set_X
##from training_set_Y import Y as training_set_Y



class TrainingDataGenerator:
    def __init__(self, AI = "minimax"):
        self.game = None
        self.X = None # X is the state
        self.Y = None # Y is the play choice
        self.AI = AI
        self.clf = None

    def initialize(self):
        if self.AI == "sklearn":
            self.clf = svm.SVR(kernel = 'linear')
            print("fitting sklearn")
            self.clf.fit(training_set_X, training_set_Y)
        self.X = open("C:\\Users\\Zhi Li\\Desktop\\CIS 667 Introduction to AI\\Project\\codes\\gaming part\\20181122 game with coin\\training_data\\training_set_X150.py", "w+")
        self.Y = open("C:\\Users\\Zhi Li\\Desktop\\CIS 667 Introduction to AI\\Project\\codes\\gaming part\\20181122 game with coin\\training_data\\training_set_Y150.py", "w+")
        self.X.write("X = [\n")
        self.Y.write("Y = [\n")

    def reset_game(self):
        self.game = MagicCardGame()
        self.game.initialize()

    def get_random_choice(self):
        lst = [0] * (Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 4 + 3 + 1)
        ##           hand0(134),                    target0(14),  battlefield0(7),battlefield_target0(7)  hero0,h1,h1, end_turn
        new_game_state,random_choice = RandomChoiceGenerator(self.game).get_random_play()
        if random_choice[0] == 1:
            lst[random_choice[1] - 1] = 1
            if random_choice[2] is not None:
                if random_choice[2] < 0:
                    if random_choice[2] == Constants.PLAYER_NICKNAME[0]:
                        lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 2 + 1 - 1] = 1
                    else:
                        lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 2 + 2 - 1] = 1
                elif random_choice[2] < self.game.state.battlefield.card0_length:
                    lst[Constants.AVAILABLE_CARDS + random_choice[2]] = 1
                elif random_choice[2] < len(self.game.state.battlefield.card_states):
                    lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND + random_choice[2]] = 1
                else:
                    raise Exception("Wrong target! target = %s" % random_choice[2])
        elif random_choice[0] == 2:
            if self.game.get_current_player() == 0:
                lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 2 + 2 + random_choice[1]] = 1
                if random_choice[2] < 0:
                    lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 4 + 3 - 1] = 1
                else:
                    target = random_choice[2] - self.game.state.battlefield.card0_length
                    lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 3 + 2 + target] = 1
            elif self.game.get_current_player() == 1:
                attacker = random_choice[2] - self.game.state.battlefield.card0_length
                lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 2 + 2 + attacker] = 1
                if random_choice[2] < 0:
                    lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 4 + 3 - 1] = 1
                else:
                    lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 3 + 2 + random_choice[2]] = 1
            else:
                raise Exception("Error!")

        elif random_choice[0] == 3:
            lst[-1] = 1
        else:
            raise Exception("Wrong input type! type = %s" % random_choice[0])
        if self.AI == "minimax":
            return lst, RandomSamplingFromState(new_game_state).do_sampling()
        elif self.AI == "sklearn":
            return lst, -1
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

                state_lst = list(self.game.get_state_tuple())
                choice_list,win_rate = self.get_random_choice()
                training_X = state_lst + choice_list
                self.X.write(str(training_X))
                self.X.write(",\n")


                if self.AI == "sklearn":
                    win_rate = self.clf.predict([training_X])
                self.Y.write(str(win_rate))
                self.Y.write(",\n")

                
                available_set = ()
                if len(self.game.available_play_cards()) != 0:
                    available_set += (1,)
                if len(self.game.available_attackers()) != 0:
                    available_set += (2,)
                available_set += (3,)
                inp = available_set[0]
                if verbose:
                    print("Action:", inp)
                if inp == 1:
                    card_id = random.choice(self.game.available_play_cards())
                    if verbose:
                        print("Playing card:", cards[card_id][0])
                    if cards[card_id][3] is not None:
                        if verbose:
                            self.game.show_available_play_card_targets(card_id)
                        target = random.choice(self.game.available_play_card_targets(card_id))
                    else:
                        target = None
                    if verbose:
                        print("Target =", target)
                    self.game.play_card(card_id, target = target)
                    if self.game.is_end():
                        break
                elif inp == 2:
                    attacker_position = random.choice(self.game.available_attackers())
                    if verbose:
                        print("Attacker: ", attacker_position)
                        self.game.show_available_attacking_targets(attacker_position)
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
        print("Winner is player %s!" % self.game.get_winner())
        

    def end_game(self):
        self.X.write("\n]")
        self.Y.write("\n]")
        self.X.close()
        self.Y.close()




if __name__ == "__main__":

    plays = 150
    play = TrainingDataGenerator(AI = "minimax")
    play.initialize()
    count = 0
    for i in range(plays):
        count += 1
        print("Play = %d" % count, end = "  ")
        play.reset_game()
        play.play_game()
    play.end_game()
    

