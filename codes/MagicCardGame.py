## this is the game part of Magic Card Game

import random
from copy import *
from cards_set import *
from effects_set import effects


#############################################################################
#############################################################################

class Constants:
    AVAILABLE_CARDS = 134  ## id of the last available card
    BONUS_CARD_ID = 0  ## id of the coin card
    
    MAX_HP = 30
    INITIAL_MANA = 0
    DECK_MAX = 30         ## The max number of cards can be in a player's deck
    HAND_MAX = 10
    MAX_MANA_UPPER_BOUND = 10

    FIRST_PLAYER = 0
    
    ## Assumption: At most two same cards are allowed in one same player's deck
    DECK_DUPLICATE_UPPER_BOUND = 2
    PLAYER_MINION_UPPERBOUND = 7
    INITIAL_FATIGUE_LEVEL = 0
    PLAYER_NICKNAME = (-10, -20)
    INITIAL_REMAINING_ATTACK_CHANCE = 0


    ## Optimize card cost curve, thus make game more playable. Reduce the randomness of the game result.(make strategy)
    CURVE_0 = 1
    CURVE_1 = 2
    CURVE_2 = 6
    CURVE_3 = 6
    CURVE_4 = 6
    CURVE_5 = 4
    CURVE_6 = 3
    CURVE_7p = 2

    HERO_HP_WEIGHT = 5
    DIVINE_SHIELD_WEIGHT = 3
    

    SORT = False
    

class MagicCardGame:
    def __init__(self, max_hp = Constants.MAX_HP, initial_mana = Constants.INITIAL_MANA, deck_max = Constants.DECK_MAX, hand_max = Constants.HAND_MAX):
        ## set state
        self.state = State(max_hp, initial_mana, deck_max, hand_max, Constants.AVAILABLE_CARDS)

    ## Initialize the state for two players
    ## 3 and 4 cards for two players respectly, the second_played player get a bonus_card
    ## DONE
    def initialize(self, first_player = Constants.FIRST_PLAYER):
        self.state.initialize()
        
    ## make a return copy and return it
    def get_deep_copy(self):
        new_game = MagicCardGame()
        
        new_game.state.deck.deck_max = self.state.deck.deck_max
        new_game.state.deck.available_cards = self.state.deck.available_cards
        new_game.state.deck.deck = deepcopy(self.state.deck.deck)
        new_game.state.deck.deck0_length = self.state.deck.deck0_length
        
        new_game.state.hand.hand = deepcopy(self.state.hand.hand)
        new_game.state.hand.hand0_length = self.state.hand.hand0_length

        lst = []
        for old_card_state in self.state.battlefield.card_states:
            new_card = CardState(old_card_state.card_id)
            new_card.current_hp = old_card_state.current_hp
            new_card.divine_shield = old_card_state.divine_shield
            new_card.remaining_attack_chance = old_card_state.remaining_attack_chance
            lst.append(new_card)
        new_game.state.battlefield.card_states = tuple(lst)
##        Attention! Some of the relatively stabled attributes are not copied!(Since tipicaly they are supose to remain unchanged.)
        
        new_game.state.battlefield.card0_length = self.state.battlefield.card0_length
        new_game.state.battlefield.max_hp = self.state.battlefield.max_hp
        new_game.state.battlefield.hero_hp = deepcopy(self.state.battlefield.hero_hp)
        new_game.state.battlefield.fatigue = deepcopy(self.state.battlefield.fatigue)
        
        new_game.state.mana.current_mana = deepcopy(self.state.mana.current_mana)
        new_game.state.mana.max_mana = deepcopy(self.state.mana.max_mana)
        
        new_game.state.current_player = self.state.current_player
        
        return new_game

    def block_opponent(self, opponent = None):
        if opponent is None:
            opponent = 1 - self.get_current_player()
        if opponent == 0:
            hand_card_amount = self.state.hand.hand0_length
        elif opponent == 1:
            hand_card_amount = len(self.state.hand.hand) - self.state.hand.hand0_length
        else:
            raise Exception("Invalid player! opponent = %s" % opponent)
        new_hand = self.state.deck.make_random_deck_for_player(hand_card_amount, opponent)
        self.state.hand.replace_hand_with(new_hand, opponent)

    def get_state_tuple(self):
        lst = [0]*((Constants.AVAILABLE_CARDS * 4) + 7 * 4 + 2 + 2)
        ##          hand0,battlefield0,h1,b1,      battlefield_cur_hp0,divine_shield0,c1,d1,     hero_cur_hp0,c1,   cur_mana0,c1
        for card_id in self.state.hand.hand[:self.state.hand.hand0_length]:
            lst[card_id - 1] += 1
        for card_id in self.state.hand.hand[self.state.hand.hand0_length:]:
            lst[Constants.AVAILABLE_CARDS * 2 + card_id - 1] += 1

        position = 1
        for card_state in self.state.battlefield.card_states[:self.state.battlefield.card0_length]:
            lst[Constants.AVAILABLE_CARDS + card_state.card_id - 1] += 1
            lst[Constants.AVAILABLE_CARDS * 4 + position - 1] = (card_state.current_hp / card_state.max_hp)
            if card_state.divine_shield:
                lst[Constants.AVAILABLE_CARDS * 4 + Constants.PLAYER_MINION_UPPERBOUND + position - 1] = 1
            position += 1
                
        position = 1
        for card_state in self.state.battlefield.card_states[self.state.battlefield.card0_length:]:
            lst[Constants.AVAILABLE_CARDS * 3 + card_state.card_id - 1] += 1
            lst[Constants.AVAILABLE_CARDS * 4 + Constants.PLAYER_MINION_UPPERBOUND * 2 + position - 1] = (card_state.current_hp / card_state.max_hp)
            if card_state.divine_shield:
                lst[Constants.AVAILABLE_CARDS * 4 + Constants.PLAYER_MINION_UPPERBOUND * 3 + position - 1] = 1
            position += 1

        lst[Constants.AVAILABLE_CARDS * 4 + Constants.PLAYER_MINION_UPPERBOUND * 4 + 1 - 1] = (self.state.battlefield.hero_hp[0] / Constants.MAX_HP)
        lst[Constants.AVAILABLE_CARDS * 4 + Constants.PLAYER_MINION_UPPERBOUND * 4 + 2 - 1] = (self.state.battlefield.hero_hp[1] / Constants.MAX_HP)

        lst[Constants.AVAILABLE_CARDS * 4 + Constants.PLAYER_MINION_UPPERBOUND * 4 + 2 + 1 - 1] = self.state.mana.current_mana[0]
        lst[Constants.AVAILABLE_CARDS * 4 + Constants.PLAYER_MINION_UPPERBOUND * 4 + 2 + 2 - 1] = self.state.mana.current_mana[1]

        return tuple(lst)

    ## This is a tuple used for machine learning trainning use.
    def get_state_tuple_without_opponent(self, player = 0):
        lst = [0]*((Constants.AVAILABLE_CARDS) + Constants.PLAYER_MINION_UPPERBOUND * 4 + 2 + 2)
        ##          hand0,           battlefield_cur_hp0,divine_shield0,c1,d1,      hero_cur_hp0,c1,   cur_mana0,c1

        lst_a = []
        lst_b = []
        
        if player == 0:
            for card_id in self.state.hand.hand[:self.state.hand.hand0_length]:
                lst[card_id - 1] += 1
        elif player == 1:
            for card_id in self.state.hand.hand[self.state.hand.hand0_length:]:
                lst[card_id - 1] += 1
        else:
            raise Exception("Wrong player!")

        if player == 0:
            lst_a = self.state.battlefield.card_states[:self.state.battlefield.card0_length]
            lst_b = self.state.battlefield.card_states[self.state.battlefield.card0_length:]
        elif player == 1:
            lst_a = self.state.battlefield.card_states[self.state.battlefield.card0_length:]
            lst_b = self.state.battlefield.card_states[:self.state.battlefield.card0_length]
        else:
            raise Exception("Wrong plyaer!")

        position = 1
        for card_state in lst_a:
            lst[Constants.AVAILABLE_CARDS + position - 1] = card_state.current_hp
            if card_state.divine_shield:
                lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND + position - 1] = Constants.DIVINE_SHIELD_WEIGHT
            position += 1
                
        position = 1
        for card_state in lst_b:
            lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 2 + position - 1] = card_state.current_hp
            if card_state.divine_shield:
                lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 3 + position - 1] = Constants.DIVINE_SHIELD_WEIGHT
            position += 1

        lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 4 + 1 - 1] = (self.state.battlefield.hero_hp[player] / Constants.MAX_HP * Constants.HERO_HP_WEIGHT)
        lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 4 + 2 - 1] = (self.state.battlefield.hero_hp[1 - player] / Constants.MAX_HP * Constants.HERO_HP_WEIGHT)

        lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 4 + 2 + 1 - 1] = self.state.mana.current_mana[player]
        lst[Constants.AVAILABLE_CARDS + Constants.PLAYER_MINION_UPPERBOUND * 4 + 2 + 2 - 1] = self.state.mana.current_mana[1 - player]

        return tuple(lst)

    def is_end(self):
        return self.state.is_end()

    def get_current_player(self):
        return self.state.current_player

    ## returns winner (0 or 1), if tie returns -1000000
    def get_winner(self):
        return self.state.get_winner()

    def needs_target(self, card_id):
        return cards[card_id][3] is not None
    
## Frequntly used player informations:
    ## return playable cards(card_id) in hand (as a tuple)
    def available_play_cards(self):
        return self.state.available_play_options(self.get_current_player())

    def show_available_play_cards(self):
        print("available_play_cards: ", self.available_play_cards())

    ## return playable cards(card_id) in hand (as a tuple)
    def available_play_card_targets(self, card_id):
        return self.state.available_play_card_targets(self.get_current_player(), card_id)

    def show_available_play_card_targets(self, card_id):
        print("available_play_card_targets: ", self.available_play_card_targets(card_id))

    ## return tuple of available attackers' positions (battlefield_position)
    def available_attackers(self):
        return self.state.available_attackers(self.get_current_player())

    def show_available_attackers(self):
        print("available_attackers: ", self.available_attackers())

    ## return tuple of available attacking targets' positions (battlefield_position)
    def available_attacking_targets(self, attacker_position):
        return self.state.available_attacking_targets(self.get_current_player(), attacker_position)

    def show_available_attacking_targets(self, attacker_position):
        print("available_attacking_targets: ", self.available_attacking_targets(attacker_position))


## Frequently used gaming operations:
    def start_turn(self):
        self.state.start_turn()
    
    def end_turn(self):
        self.state.end_turn()

    ## draw card from deck
    def draw(self, player = None):
        if player is None:
            player = self.get_current_player()
        self.state.draw(player)

    def attack(self, attacker_position, target_position):
        self.state.attack(attacker_position, target_position)

    ## play card from hand
    def play_card(self, card_id, target = None, player = None):
        if player is None:
            player = self.get_current_player()
        self.state.play_card(player, card_id, target)

    def end_game(self):
        self.show_game_result()
    
## Frequently used printing options
    def show_state(self):
        print("Current player is: %s" % self.get_current_player())
        self.show_hp(1)
        self.show_mana(1)
        print()
        self.show_hand(1)
        print('*' * 200)
        self.show_battlefield()
        self.show_hand(0)
        self.show_hp(0)
        self.show_mana(0)
        print()
        print('*' * 200)
        print('*' * 200)
        
    ## show the cards in hand for the current player
    def show_hand(self, player = None):
        if player is None:
            player = self.get_current_player()
        self.state.hand.print(player)

    ## This dunction is only used for debug(It won't make sence to allow any player see the deck sequence!)
    def show_deck(self, player = None):
        if player is None:
            player = self.get_current_player()        
        print(self.state.get_deck(player))

    ## show the minions on the battle field
    def show_battlefield(self):
        self.state.battlefield.print()

    def show_hp(self, player = None):
        if player is None:
            player = self.get_current_player()
        print("hp = %s " % self.state.battlefield.get_hp(player), end = " ")

    def show_mana(self, player = None):
        if player is None:
            player = self.get_current_player()
        print("mana = ", self.state.mana.get_mana(player), end = " ")

    def show_game_result(self):
        print("-" * 100)
        print("-" * 100)
        print("Winner is player %s!" % self.get_winner())
        

#############################################################################
#############################################################################
## State part
class State:
    def __init__(self, max_hp, initial_mana, deck_max, hand_max, available_cards):
        self.deck = Deck(deck_max, available_cards)
        self.hand = Hand()
        self.battlefield = Battlefield(max_hp)
        self.mana = Mana(initial_mana)
        self.current_player = Constants.FIRST_PLAYER

    ## draw 3 cards for the first player, draw 4 cards and a coin for the second player
    def initialize(self):
        self.deck.initialize()
        for i in range(3):
            self.draw(self.current_player)
        for i in range(4):
            self.draw(1 - self.current_player)
##            $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ // give bonus hand now
        self.hand.add_hand(1 - self.current_player, Constants.BONUS_CARD_ID)

## State:Return sepcific states
    ## Used to determine whether the game is over
    ## DONE
    def is_end(self):
        if self.battlefield.get_hp(0) <= 0 or self.battlefield.get_hp(1) <= 0:
            return True
        else:
            return False
        
    ## player == -1 means get two players' hand
    def get_hand(self, player = -1):
        return self.hand.get_hand(player)

    ## player == -1 means get two players' deck
    def get_deck(self, player = -1):
        return self.deck.get_deck(player)

    ## Return -1000000 if tie (Two hero die simultaneously)
    def get_winner(self):
        if self.battlefield.get_hp(0) <= 0 and self.battlefield.get_hp(1) <= 0:
            return -1000000 ## tie
        elif self.battlefield.get_hp(0) <= 0:
            return 1
        elif self.battlefield.get_hp(1) <= 0:
            return 0



## State:Actions
    ## start turn
    def start_turn(self):
        self.draw(self.current_player)
        self.mana.start_turn(self.current_player)
        self.battlefield.reset_attack_chances(self.current_player)

    ## end turn
    def end_turn(self):
        self.current_player = 1 - self.current_player
        
    ## Draw a card from the deck(very frequent used API)
    def draw(self, player):
        if self.deck.is_empty(player):
            ## deal with fatigue
            self.battlefield.fatigue_plus(player)
        else:
            self.hand.add_hand(player, self.deck.remove_deck(player))
    
    ## attack
    def attack(self, attacker_position, target_position):
        self.battlefield.attack(attacker_position, target_position)
    
    ## play card from hand,
    def play_card(self, player, card_id, target):
        if (not self.is_play_card_target_valid(player, card_id, target)):
            raise Exception("Illegal target!")
        
        ## use effect(effect_name, effect_parameter, player, target) to call effects
        ## call effect
        self.effect(cards[card_id][6], cards[card_id][7], player, target)
        self.effect(cards[card_id][8], cards[card_id][9], player, target)

        ## place card if card_type is minion
        if cards[card_id][1] == 1:
            self.battlefield.add_card(player, card_id)

        ## remove card from hand
        self.hand.remove_hand(player, card_id)

        ## mana cost
        self.mana.cost(player, cards[card_id][2])

## State:Algorithm related methods
    ## return tuple of available attackers' positions
    def available_attackers(self, player):
        return self.battlefield.available_attackers(player)

    ## return tuple of available attacking targets' positions
    def available_attacking_targets(self, player, attacker_position):
        return self.battlefield.available_attacking_targets(player, attacker_position)
        
    ## available play options, return a tuple of card_id
    def available_play_options(self, player):
        lst = []
        for card_id in self.hand.get_hand(player):
            ## check if mana is sufficient
            if not (self.mana.is_sufficient(player, card_id)):
                continue
            ## check if have valid target
            if not((cards[card_id][3] is None) or (self.available_play_card_targets(player, card_id)[0] is not None)):
                continue
            ## valid -> add to list
            lst.append(card_id)
        return tuple(lst)

    ## available targets set for spells and minion effects only(cannot be used when doing attack)
    def available_play_card_targets(self, player, card_id):
        res = ()
        if cards[card_id][3] == None:
            res += (None,)
        elif cards[card_id][3] == 0:
            ## aming hero only
            target_restriction = effects[cards[card_id][6]][2]
            if target_restriction == 2:
                res += (Constants.PLAYER_NICKNAME[0],)
                res += (Constants.PLAYER_NICKNAME[1],)
            elif target_restriction == 0:
                res += (Constants.PLAYER_NICKNAME[player],)
            elif target_restriction == 1:
                res += (Constants.PLAYER_NICKNAME[1 - player],)
            else:
                raise Exception("Target bug!")
        elif cards[card_id][3] == 1:
            ## aming minions only
            target_restriction = effects[cards[card_id][6]][2]
            if target_restriction == 2:
                res = self.battlefield.get_battlefield_positions()
            elif target_restriction == 0:
                res = self.battlefield.get_battlefield_positions(player)
            elif target_restriction == 1:
                res = self.battlefield.get_battlefield_positions(1 - player)
            else:
                raise Exception("Target bug!")
        elif cards[card_id][3] == 2:
            ## aming hero or minions
            target_restriction = effects[cards[card_id][6]][2]
            if target_restriction == 2:
                res += (Constants.PLAYER_NICKNAME[0],)
                res += (Constants.PLAYER_NICKNAME[1],)
            elif target_restriction == 0:
                res += (Constants.PLAYER_NICKNAME[player],)
            elif target_restriction == 1:
                res += (Constants.PLAYER_NICKNAME[1 - player],)
            else:
                raise Exception("Target bug!")
            
            if target_restriction == 2:
                res = self.battlefield.get_battlefield_positions()
            elif target_restriction == 0:
                res = self.battlefield.get_battlefield_positions(player)
            elif target_restriction == 1:
                res = self.battlefield.get_battlefield_positions(1 - player)
            else:
                raise Exception("Target bug!")
        else:
            raise Exception("Error when trying to get target_type!")
        if(len(res) == 0):
            res += (None,)
        return res

    def is_play_card_target_valid(self, player, card_id, target):
        if cards[card_id][3] == None:
            return target == None
        elif cards[card_id][3] == 0:
            ## hero only
            target_restriction = effects[cards[card_id][6]][2]
            if target_restriction == 2:
                return target == Constants.PLAYER_NICKNAME[0] or target == Constants.PLAYER_NICKNAME[1]
            elif target_restriction == 0:
                return target == Constants.PLAYER_NICKNAME[player]
            elif target_restriction == 1:
                return target == Constants.PLAYER_NICKNAME[1 - player]
            else:
                raise Exception("Target restriction Error!")                
        elif cards[card_id][3] == 1:
            ## minions only
            target_restriction = effects[cards[card_id][6]][2]
            if target_restriction == 2:
                return target >= 0 and target < len(self.battlefield.get_battlefield()[0])
            elif (target_restriction == 0 and player == 0) or (target_restriction == 1 and player == 1):
                return target >= 0 and target < self.battlefield.get_battlefield()[1]
            elif (target_restriction == 0 and player == 1) or (target_restriction == 1 and player == 0):
                return target >= self.battlefield.get_battlefield()[1] and target < len(self.battlefield.get_battlefield()[0])
            else:
                raise Exception("Target restriction Error!")   
        elif cards[card_id][3] == 2:
            ## minions or hero
            target_restriction = effects[cards[card_id][6]][2]
            if target_restriction == 2:
                hero = (target == Constants.PLAYER_NICKNAME[0] or target == Constants.PLAYER_NICKNAME[1])
            elif target_restriction == 0:
                hero = (target == Constants.PLAYER_NICKNAME[player])
            elif target_restriction == 1:
                hero = (target == Constants.PLAYER_NICKNAME[1 - player])
            else:
                raise Exception("Target restriction Error!")
            
            if target_restriction == 2:
                minion = (target >= 0 and target < len(self.battlefield.get_battlefield()[0]))
            elif (target_restriction == 0 and player == 0) or (target_restriction == 1 and player == 1):
                minion = (target >= 0 and target < self.battlefield.get_battlefield()[1])
            elif (target_restriction == 0 and player == 1) or (target_restriction == 1 and player == 0):
                minion = (target >= self.battlefield.get_battlefield()[1] and target < len(self.battlefield.get_battlefield()[0]))
            else:
                raise Exception("Target restriction Error!")
            
            return hero or minion
        else:
            raise Exception("Error when trying to get target_type!")

    ####################
    ## Effect functions:
## State:Effect functions
    def deal_damage(self, effect_name, effect_parameter, player, target):
        self.battlefield.target_take_damage(target, effect_parameter)
     
    def aoe(self, effect_name, effect_parameter, player, target):
        ## effect_parameter = damage amount
        ## enemy characters take damage
        ## taget is None
        if player == 1:
            self.battlefield.target_take_damage(Constants.PLAYER_NICKNAME[0], effect_parameter)
            _, b0 = self.battlefield.get_battlefield()
            for i in range(0, b0, -1):
                self.battlefield.target_take_damage(i, effect_parameter)
        elif player == 0:
            self.battlefield.target_take_damage(Constants.PLAYER_NICKNAME[1], effect_parameter)
            b, b0 = self.battlefield.get_battlefield()
            for i in range(b0, len(b), -1):
                self.battlefield.target_take_damage(i, effect_parameter)
        else:
            raise Exception("Invalid player!")
             
    def heal(self, effect_name, effect_parameter, player, target):
        self.battlefield.target_get_heal(target, effect_parameter)
     
    def aoe_heal(self, effect_name, effect_parameter, player, target):
        ## effect_parameter = healing amount
        ## friendly characters get heal
        ## taget is None
        if player == 0:
            self.battlefield.target_get_heal(Constants.PLAYER_NICKNAME[0], effect_parameter)
            _, b0 = self.battlefield.get_battlefield()
            for i in range(0, b0):
                self.battlefield.target_get_heal(i, effect_parameter)
        elif player == 1:
            self.battlefield.target_get_heal(Constants.PLAYER_NICKNAME[1], effect_parameter)
            b, b0 = self.battlefield.get_battlefield()
            for i in range(b0, len(b)):
                self.battlefield.target_get_heal(i, effect_parameter)
        else:
            raise Exception("Invalid player!")        
     
    def draw_card(self, effect_name, effect_parameter, player, target):
        ## player is the player who draw the cards
        ## target is None
        for i in range(effect_parameter):
            self.draw(player)
     
    def summon(self, effect_name, effect_parameter, player, target):
        ## effect_parameter is summoned card_id
        ## palyer is the one get the summoned minion
        ## target is None
        self.battlefield.add_card(player, effect_parameter)
     
    def transform_minion(self, effect_name, effect_parameter, player, target):
        ## effect_parameter is the card_id of the new minion
        ## player is Override in the function
        ## target is position that the minion being replaced
        _, b0 = self.battlefield.get_battlefield()
        if target < b0:
            player = 0
        else:
            player = 1
        self.battlefield.remove_card(target)
        self.battlefield.add_card(player, effect_parameter)
     
    def take_control_minion(self, effect_name, effect_parameter, player, target):
        ## effect_parameter is None
        ## player is Overrided in the function
        ## player will be the one who get control of the target minion at the end
        ## target is the position of a minion who will be switch to the opponent's battlefield
        _, b0 = self.battlefield.get_battlefield()
        if target < b0:
            player = 1
        else:
            player = 0
        self.battlefield.add_card(player, effect_parameter, self.battlefield.remove_card(target))
     
    def kill_minion(self, effect_name, effect_parameter, player, target):
        ## target is the position that minion get removed
        self.battlefield.remove_card(target)
     
    def clear_board(self, effect_name, effect_parameter, player, target):
        while (not self.battlefield.is_empty()):
            self.battlefield.remove_card(0)

    def gain_mana(self, effect_name, effect_parameter, player, target):
        self.mana.add_mana(player, effect_parameter)

    def non_effect(self, effect_name, effect_parameter, player, target):
        return
     
    def effect(self, effect_name, effect_parameter, player, target): ## player is the current player number (0, 1)
        switcher = {
            "deal_damage": self.deal_damage,
            "kill_minion": self.kill_minion,
            "take_control_minion": self.take_control_minion,
            
            "heal": self.heal,
            
            "transform_minion": self.transform_minion,
            
            "aoe": self.aoe,
            "aoe_heal": self.aoe_heal,
            "draw_card": self.draw_card,
            "summon": self.summon,
            "gain_mana": self.gain_mana,
            
            "clear_board": self.clear_board,


            "taunt": self.non_effect,
            "divine_shield": self.non_effect,
            "charge": self.non_effect,
            "windfury": self.non_effect,
            None: self.non_effect
        }
        if effect_name not in switcher:
            print("effect_name = %s" % effect_name)
            raise Exception("No such effect available!")
        func = switcher.get(effect_name, lambda: "Wrong effect_name")
        func(effect_name, effect_parameter, player, target)
    
    ## use effect(effect_name, effect_parameter, player, target) to call effects
    ## End effect Functions
                
        
#############################################################################
#############################################################################
## Deck states and operations
class Deck:
    def __init__(self, deck_max, available_cards):
        self.deck_max = deck_max
        self.available_cards = available_cards
        self.deck = ()  ## (11,12,13,14,15,16,17,18,19,110,21,22,23,24,25)
        self.deck0_length = 0  ## Remember to update deck0_length in every API in this class!!!!!!!!!!
        
    def initialize(self):
        self.make_optimal_deck(self.deck_max, self.available_cards)

## Deck:States
    def is_empty(self, player):
        if player == 0:
            return self.deck0_length == 0
        elif player == 1:
            return (len(self.deck) - self.deck0_length) == 0
        else:
            raise Exception("Input player number has to be 0 or 1 in Deck.is_empty! But it was %d" % player)

    def get_deck(self, player = -1):
        if player == -1:
            return self.deck, self.deck0_length
        if player == 0:
            return self.deck[:self.deck0_length]
        elif player == 1:
            return self.deck[self.deck0_length:]
        else:
            raise Exception("Input player number has to be 0 or 1 in Deck.get_deck! But it was %d" % player)

## Deck:Actions
    ## seldom used method
    def add_deck(self, player, card_id, position = None):
        if position is None:
            position = ((1 - player) * (self.deck0_length - 1) + player * (len(self.deck) - 1))
        if player != 0 and player != 1:
            raise Exception("Input player number has to be 0 or 1 in Deck.add_deck! But it was %d" % player)                  
        if position < 0 or position >= len(self.state):
            raise Exception("Input position in Deck.add_deck is out of bound! len(deck) = %d, position = %d" % (len(self.deck), position))

        self.deck = self.deck[:position] + (card_id,) + self.deck[position + 1:]
        self.shuffle()
        if player == 0:
            self.deck0_length += 1

    ## remove_deck by default remove the last card in the player's deck
    def remove_deck(self, player, position = None):
        if position is None:
            position = ((1 - player) * (self.deck0_length - 1) + player * (len(self.deck) - 1))
        if player != 0 and player != 1:
            raise Exception("Input player number has to be 0 or 1 in Deck.remove_deck! But it was %d" % player)              
        if position < 0 or position >= len(self.deck):
            raise Exception("Input position in Deck.remove_deck is out of bound! len(deck) = %d, position = %d" % (len(self.deck), position))
        
        position_card_id = self.deck[position]
        self.deck = self.deck[:position] + self.deck[position + 1:]
        if player == 0:
            self.deck0_length -= 1
        return position_card_id
    
    ## keep the cards in deck with random order in card_id
    def shuffle(self):
        lst0 = list(self.deck[:self.deck0_length])
        lst1 = list(self.deck[self.deck0_length:])
        lst0 = random.sample(lst0, len(lst0))
        lst1 = random.sample(lst1, len(lst1))
        self.deck = tuple(lst0 + lst1)

    ## Used to initial deck with a random collection
    def make_random_deck(self, deck_max, available_cards):
        if len(self.deck) != 0:
            raise Exception("Deck should be empty when using 'make_random_deck'")
        for i in range(2):
            self.deck += tuple(random.sample(range(available_cards), deck_max//2) + random.sample(range(available_cards), deck_max - deck_max//2))
        self.deck0_length = deck_max

    ## Used to block the AI player from seeing the opponent's deck
    ## player's deck will be inplaced
    def make_random_deck_for_player(self, hand_card_amount, player):
        c = CardClassify()
        if player == 0:
            deck0 = []
            deck1 = ()
            hand0 = []
            
            deck1 = self.deck[self.deck0_length:]
            deck0 += (random.sample(c.cost_0, Constants.CURVE_0//2) + random.sample(c.cost_0, Constants.CURVE_0 - Constants.CURVE_0//2))
            deck0 += (random.sample(c.cost_1, Constants.CURVE_1//2) + random.sample(c.cost_1, Constants.CURVE_1 - Constants.CURVE_1//2))
            deck0 += (random.sample(c.cost_2, Constants.CURVE_2//2) + random.sample(c.cost_2, Constants.CURVE_2 - Constants.CURVE_2//2))
            deck0 += (random.sample(c.cost_3, Constants.CURVE_3//2) + random.sample(c.cost_3, Constants.CURVE_3 - Constants.CURVE_3//2))
            deck0 += (random.sample(c.cost_4, Constants.CURVE_4//2) + random.sample(c.cost_4, Constants.CURVE_4 - Constants.CURVE_4//2))
            deck0 += (random.sample(c.cost_5, Constants.CURVE_5//2) + random.sample(c.cost_5, Constants.CURVE_5 - Constants.CURVE_5//2))
            deck0 += (random.sample(c.cost_6, Constants.CURVE_6//2) + random.sample(c.cost_6, Constants.CURVE_6 - Constants.CURVE_6//2))
            deck0 += (random.sample(c.cost_7p, Constants.CURVE_7p//2) + random.sample(c.cost_7p, Constants.CURVE_7p - Constants.CURVE_7p//2))

            hand0 = random.sample(deck0, hand_card_amount)
            for card_id in hand0:
                deck0.remove(card_id)
            while len(deck0) > self.deck0_length:
                del deck0[random.randint(0, len(deck0) - 1)]

            self.deck = tuple(deck0) + deck1
            return tuple(hand0)
            
        elif player == 1:

            deck0 = ()
            deck1 = []
            hand1 = []
            
            deck0 = self.deck[:self.deck0_length]
            deck1 += (random.sample(c.cost_0, Constants.CURVE_0//2) + random.sample(c.cost_0, Constants.CURVE_0 - Constants.CURVE_0//2))
            deck1 += (random.sample(c.cost_1, Constants.CURVE_1//2) + random.sample(c.cost_1, Constants.CURVE_1 - Constants.CURVE_1//2))
            deck1 += (random.sample(c.cost_2, Constants.CURVE_2//2) + random.sample(c.cost_2, Constants.CURVE_2 - Constants.CURVE_2//2))
            deck1 += (random.sample(c.cost_3, Constants.CURVE_3//2) + random.sample(c.cost_3, Constants.CURVE_3 - Constants.CURVE_3//2))
            deck1 += (random.sample(c.cost_4, Constants.CURVE_4//2) + random.sample(c.cost_4, Constants.CURVE_4 - Constants.CURVE_4//2))
            deck1 += (random.sample(c.cost_5, Constants.CURVE_5//2) + random.sample(c.cost_5, Constants.CURVE_5 - Constants.CURVE_5//2))
            deck1 += (random.sample(c.cost_6, Constants.CURVE_6//2) + random.sample(c.cost_6, Constants.CURVE_6 - Constants.CURVE_6//2))
            deck1 += (random.sample(c.cost_7p, Constants.CURVE_7p//2) + random.sample(c.cost_7p, Constants.CURVE_7p - Constants.CURVE_7p//2))

            hand1 = random.sample(deck1, hand_card_amount)
            for card_id in hand1:
                deck1.remove(card_id)
            while len(deck1) > (len(self.deck) - self.deck0_length):
                del deck1[random.randint(0, len(deck1) - 1)]

            self.deck = deck0 + tuple(deck1)
            return tuple(hand1)

        else:
            raise Exception("Invalid Player! player = %s" % player)
        


    def make_optimal_deck(self, deck_max, available_cards):
        if len(self.deck) != 0:
            raise Exception("Deck should be empty when using 'make_optimal_deck'")
        c = CardClassify()
        for i in range(2):
            self.deck += tuple(random.sample(c.cost_0, Constants.CURVE_0//2) + random.sample(c.cost_0, Constants.CURVE_0 - Constants.CURVE_0//2))
            self.deck += tuple(random.sample(c.cost_1, Constants.CURVE_1//2) + random.sample(c.cost_1, Constants.CURVE_1 - Constants.CURVE_1//2))
            self.deck += tuple(random.sample(c.cost_2, Constants.CURVE_2//2) + random.sample(c.cost_2, Constants.CURVE_2 - Constants.CURVE_2//2))
            self.deck += tuple(random.sample(c.cost_3, Constants.CURVE_3//2) + random.sample(c.cost_3, Constants.CURVE_3 - Constants.CURVE_3//2))
            self.deck += tuple(random.sample(c.cost_4, Constants.CURVE_4//2) + random.sample(c.cost_4, Constants.CURVE_4 - Constants.CURVE_4//2))
            self.deck += tuple(random.sample(c.cost_5, Constants.CURVE_5//2) + random.sample(c.cost_5, Constants.CURVE_5 - Constants.CURVE_5//2))
            self.deck += tuple(random.sample(c.cost_6, Constants.CURVE_6//2) + random.sample(c.cost_6, Constants.CURVE_6 - Constants.CURVE_6//2))
            self.deck += tuple(random.sample(c.cost_7p, Constants.CURVE_7p//2) + random.sample(c.cost_7p, Constants.CURVE_7p - Constants.CURVE_7p//2))
        self.deck0_length = deck_max
        self.shuffle()
        
            
#############################################################################
#############################################################################
## Hand States and operations
class Hand:
    def __init__(self):
        self.hand = () ## (11,12,15,21,22,23,24,25)
        self.hand0_length = 0 ## Remember to update in every API in this class!!!!!!

## Hand:States
    def is_empty(self, player):
        if player == 0:
            return self.hand0_length == 0
        elif player == 1:
            return (len(self.hand) - self.hand0_length) == 0
        else:
            raise Exception("Input player number has to be 0 or 1 in hand.is_empty! But it was %d" % player)

    ## Return the card_id in hand
    def get_hand(self, player = -1):
        if player == -1:
            return self.hand, self.hand0_length
        elif player == 0:
            return self.hand[:self.hand0_length]
        elif player == 1:
            return self.hand[self.hand0_length:]
        else:
            raise Exception("Player have to be 0 or 1 when calling get_hand! But is was %d" % player)

    ## print cards in hand
    def print(self, player):
        p = self.get_hand(player)
        for card_id in p:
            print("{:^26}".format(str(card_id) + " " + str(cards[card_id][0])), end = "\t")
        print()
        for card_id in p:
            if cards[card_id][1] == 1:
                print("Cost:{:^4}   AT:{:^4}  HP:{:^4}".format(cards[card_id][2], cards[card_id][4], cards[card_id][5]), end = "\t")
            else:
                print("         Cost:{:^3}         ".format(cards[card_id][2]), end = "\t")
        print()
        for card_id in p:
            st = ""
            if cards[card_id][6] is not None:
                st += cards[card_id][6]
                st += " "
            if cards[card_id][7] is not None:
                st += str(cards[card_id][7])
                st += " "
            if cards[card_id][8] is not None:
                st += cards[card_id][8]
                st += " "
            if cards[card_id][9] is not None:
                st += str(cards[card_id][9])
                st += " "
            print("{:^26}".format(st), end = "\t")
        print()

## Hand:Actions
    def add_hand(self, player, card_id):
        if player == 0:
            self.hand = (card_id,) + self.hand
            self.hand0_length += 1
        elif player == 1:
            self.hand += (card_id,)
        else:
            raise Exception("Input player number has to be 0 or 1 in add_hand! But it was %d" % player)
        if Constants.SORT is True:
            self.sort()
        
    def remove_hand(self, player, card_id):
        if player != 0 and player != 1:
            raise Exception("Input player number has to be 0 or 1 in remove_hand! But it was %d" % player)
        for position in range(self.hand0_length * player, self.hand0_length * player + len(self.get_hand(player))):
            if self.hand[position] == card_id:
                break
        if self.hand[position] != card_id:
            raise Exception('Player %d do not have card with card_id = %d' % (player, card_id))
        self.hand = self.hand[: position] + self.hand[position + 1:]
        if player == 0:
            self.hand0_length -= 1

    def replace_hand_with(self, new_hand, player):
        if player == 0:
            self.hand = new_hand + self.hand[self.hand0_length:]
        elif player == 1:
            self.hand = self.hand[:self.hand0_length] + new_hand
        else:
            raise Exception("Invalid Player! player = %s" % player)
        if Constants.SORT is True:
            self.sort()
        
            
    ## keep the cards in hand with ascending order in card_id
    def sort(self):
        lst0 = []
        lst1 = []
        lst = []
        for i in self.hand[:self.hand0_length]:
            lst0.append((i, cards[i][2]))
        for i in self.hand[self.hand0_length:]:
            lst1.append((i, cards[i][2]))
        lst0 = sorted(lst0, key = lambda c: c[1])
        lst1 = sorted(lst1, key = lambda c: c[1])
        for i in lst0:
            lst.append(i[0])
        for i in lst1:
            lst.append(i[0])
        self.hand = tuple(lst)

        
#############################################################################
#############################################################################
## This class manage cards attacking and hp changing
class Battlefield:
    
    def __init__(self, max_hp):
        self.card_states = ()
        self.card0_length = 0
        self.max_hp = max_hp
        self.hero_hp = (max_hp, max_hp)
        self.fatigue = (Constants.INITIAL_FATIGUE_LEVEL, Constants.INITIAL_FATIGUE_LEVEL)

## Battlefield:States
    def is_empty(self):
        return len(self.card_states) == 0

    def is_full(self, player):
        if player ==0:
            return self.card0_length >= Constants.PLAYER_MINION_UPPERBOUND
        elif player == 1:
            return (len(self.card_states) - self.card0_length) >= Constants.PLAYER_MINION_UPPERBOUND
        else:
            raise Exception("Input player number has to be 0 or 1 in Battlefield.is_full! But it was %d" % player)
    
    def get_battlefield(self):
        return self.card_states, self.card0_length

    def get_state(self, player):
        if player == 0:
            return self.card_states[:self.card0_length]
        elif player == 1:
            return self.card_states[self.card0_length:]
        else:
            raise Exception("Illegal player number!")
    
    def get_hp(self, player):
        return self.hero_hp[player]

    ## player == -1 prints the whole field
    ##     8 7 6
    ##  0 1 2 3 4 5
    def print(self, player = -1):
        if player == -1:
            p1 = self.get_state(0)
            p2 = self.get_state(1)
            p2 = p2[::-1]
            for p in (p2, p1):
                for card_state in p:
                    print("{:^26}".format(card_state.get_name()), end = "\t")
                print()
                for card_state in p:
                    print(" AT: {:^9} HP: {:^9}".format(card_state.get_attack(), card_state.get_hp()), end = "\t")
                print()
                for card_state in p:
                    st = ""
                    if card_state.taunt:
                        st += "taunt "
                    if card_state.divine_shield:
                        st += "div_shield "
                    if card_state.charge:
                        st += "charge "
                    if card_state.windfury:
                        st += "windfury "
                    print("{:^26}".format(st), end = "\t")
                print()
                print('*' * 200)

    def get_battlefield_positions(self, player = -1):
        lst = []
        if player == -1:
            for i in range(len(self.card_states)):
                lst.append(i)
        elif player == 0:
            for i in range(self.card0_length):
                lst.append(i)
        elif player == 1:
            for i in range(self.card0_length, len(self.card_states)):
                lst.append(i)
        else:
            raise Exception("Illegal player input!")
        return tuple(lst)

## Battlefield:Actions
    def add_card(self, player, card_id, card_state = None):
        if player == 0:
            if self.is_full(player):
##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
##                print("Warning!!!  Card(card_id = %s, card_name = %s) cannot be placed since the battlefield for player %s is full!" % (card_id, cards[card_id][0], player))
                p = 0
            else:
                if card_state is None:
                    self.card_states = (CardState(card_id),) + self.card_states
                else:
                    self.card_states = (card_state,) + self.card_states
                self.card0_length += 1
                if Constants.SORT is True:
                    self.sort()
        elif player == 1:
            if self.is_full(player):
##                $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
##                print("Warning!!!  Card(card_id = %s, card_name = %s) cannot be placed since the battlefield for player %s is full!" % (card_id, cards[card_id][0], player))
                p = 0
            else:
                if card_state is None:
                    self.card_states = self.card_states + (CardState(card_id),)
                else:
                    self.card_states = self.card_states + (card_state,)
                if Constants.SORT is True:
                    self.sort()
        else:
            raise Exception("Input player number has to be 0 or 1 in Battlefield.add_card! But it was %d" % player)

    def remove_card(self, position):
        if position < 0 or position >= len(self.card_states):
            raise Exception("Position out of bound in Battlefield.emove_card.")
        removed_card = self.card_states[position]
        self.card_states = self.card_states[:position] + self.card_states[position + 1:]        
        if position < self.card0_length:
            self.card0_length -= 1
        return removed_card

    ## sort battle field by card_cost
    def sort(self):
        lst0 = list(self.card_states[:self.card0_length])
        lst1 = list(self.card_states[self.card0_length:])
        lst0 = sorted(lst0, key = lambda c: cards[c.card_id][2])
        lst1 = sorted(lst1, key = lambda c: cards[c.card_id][2])
        self.card_states = tuple(lst0 + lst1)
    
    ## update the self.card_states after attack action
    ## attacker_position, target_position
    def attack(self, attacker_position, target_position):
        attacker_attack = self.card_states[attacker_position].get_attack()
        ## attackng cosumes 1 attack_chance
##        print("Attack_chance$$$$$$$$$$$$$$$$",self.card_states[attacker_position].remaining_attack_chance)
        self.card_states[attacker_position].reduce_attack_chance()
##        print("Attack_chance$$$$$$$$$$$$$$$$",self.card_states[attacker_position].remaining_attack_chance)
        
        ## if target is hero
        if target_position < -1:
            if target_position == Constants.PLAYER_NICKNAME[0]:
                self.hero_take_damage(0, attacker_attack)
            elif target_position == Constants.PLAYER_NICKNAME[1]:
                self.hero_take_damage(1, attacker_attack)
            else:
                raise Exception("Invalid target position!")
        else: 
            target_attack = self.card_states[target_position].get_attack()
            self.card_states[target_position].take_damage(attacker_attack)
            self.card_states[attacker_position].take_damage(target_attack)        
            ## make position 1
            ## to avoid position changed after deleting the first position
            pos1 = min(attacker_position, target_position)
            pos2 = max(attacker_position, target_position)
            if self.card_states[pos2].is_dead():
                self.remove_card(pos2)
            if self.card_states[pos1].is_dead():
                self.remove_card(pos1)
            
    def reset_attack_chances(self, player):
        if player == 0:
            for card_state in self.card_states[:self.card0_length]:
                card_state.reset_attack_chance()
        if player == 1:
            for card_state in self.card_states[self.card0_length:]:
                card_state.reset_attack_chance()

    ## Tipically this method is called when one player with an empty deck try to draw_card
    def fatigue_plus(self, player):
        lst = list(self.fatigue)
        lst[player] += 1
        self.hero_take_damage(player, lst[player])
        self.fatigue = tuple(lst)


    ## when a hero takes damage, should check whether end game
    def hero_take_damage(self, player, amount):
        lst = list(self.hero_hp)
        lst[player] -= amount
        self.hero_hp = tuple(lst)
        
    ## when a hero get heal, it will check whether hp will be > self.max_hp
    def hero_get_heal(self, player, amount):
        lst = list(self.hero_hp)
        lst[player] = max(self.max_hp, lst[player] + amount)
        self.hero_hp = tuple(lst)

    ## target take pure damage
    def target_take_damage(self, target_position, amount):
        if target_position < -1:
            if target_position == Constants.PLAYER_NICKNAME[0]:
                self.hero_take_damage(0, amount)
            elif target_position == Constants.PLAYER_NICKNAME[1]:
                self.hero_take_damage(1, amount)
            else:
                raise Exception("Invalid target_position!")
        else:
            ## deal with divine_shield
            if self.card_states[target_position].divine_shield:
                self.card_states[target_position].divine_shield = False
                return
            else:
                self.card_states[target_position].take_damage(amount)
            if self.card_states[target_position].is_dead():
                self.remove_card(target_position)

    ## target get heal
    def target_get_heal(self, target_position, amount):
        if target_position < -1:
            if target_position == Constants.PLAYER_NICKNAME[0]:
                self.hero_get_heal(0, amount)
            elif target_position == Constants.PLAYER_NICKNAME[1]:
                self.hero_get_heal(1, amount)
        else:
            self.card_states[target_position].get_heal(amount)
            
            if self.card_states[target_position].is_dead():
                self.remove_card(target_position)

## Battlefield:Algorithm related methods
    ## return a tuple of positions of available action minions
    def available_attackers(self, player):
        lst = []
        if player == 0:
            for i in range(0, self.card0_length):
                try:
                    p = self.card_states[i]
                except:
                    print("self.card_states.length = %s" % len(self.card_states))
                    print("self.card0_length = %s" % self.card0_length)
                    print("i = %s" % i)
                if self.card_states[i].is_available_attacker():
                    lst.append(i)
        elif player == 1:
            for i in range(self.card0_length, len(self.card_states)):
                if self.card_states[i].is_available_attacker():
                    lst.append(i)
        else:
            raise Exception("Wrong player input!")
        return tuple(lst)
    
    ## return a tuple of positions of available targets who can be attacked be the giving attacker
    def available_attacking_targets(self, player, attacker_position):
        lst = []
        if attacker_position < 0 or attacker_position >= len(self.card_states):
            raise Exception("Wrong attacker_position!")
        if player == 1:
            ## deal with taunt
            for i in range(0, self.card0_length):
                if self.card_states[i].is_taunt():
                    lst.append(i)
            ## if no taunt
            if len(lst) == 0:
                for i in range(0, self.card0_length):
                    lst.append(i)
                ## Constants.PLAYER_NICKNAME[0] indicates the opponent hero(player 0's hero)
                lst.append(Constants.PLAYER_NICKNAME[0])
        else:
            ## deal with taunt
            for i in range(self.card0_length, len(self.card_states)):
                if self.card_states[i].is_taunt():
                    lst.append(i)
            ## if no taunt
            if len(lst) == 0:
                for i in range(self.card0_length, len(self.card_states)):
                    lst.append(i)
                ## Constants.PLAYER_1_NICKNAME indicates the opponent hero(player 1's hero)
                lst.append(Constants.PLAYER_NICKNAME[1])
        return tuple(lst)
                

#############################################################################
#############################################################################
## Only those minion cards who had been played will be record in this class
class CardState:
    
    def __init__(self, card_id):
        self.card_id = card_id
        self.card_name = cards[card_id][0]

        if cards[card_id][1] != 1:
            raise Exception("Only minion cards can be placed on Battlefield! The type of this card is: %s" % cards[card_id][1])
        ## card_type = 1    no needed here
        ## card_cost        no needed here
        ## target_type      no needed here
        self.attack = cards[card_id][4]
        self.max_hp = cards[card_id][5]
        self.current_hp = self.max_hp
        self.effect1 = (cards[card_id][6], cards[card_id][7])
        self.effect2 = (cards[card_id][8], cards[card_id][9])
        self.notes = cards[card_id][-1]
        ## cards:
        ## card_id: (card_name, card_type, card_cost, target_type, attack, hitpoint, effect1, effect1_amount, effect2, effect2_amount, Notes)
        ##            0          1          2          3           4       5         6         7              8        9               10
        ## card_type:     0: spell       1: minion
        ## target_type:   0: hero only   1: minion only   2: any enemy

        ## deal with taunt
        self.taunt = (self.effect1[0] == "taunt" or self.effect2[0] == "taunt")
        ## deal with divine_shield
        self.divine_shield = (self.effect1[0] == "divine_shield" or self.effect2[0] == "divine_shield")
        self.remaining_attack_chance = Constants.INITIAL_REMAINING_ATTACK_CHANCE
        ## deal with charge
        self.charge = (self.effect1[0] == "charge" or self.effect2[0] == "charge")
        self.windfury = (self.effect1[0] == "windfury" or self.effect2[0] == "windfury")
        if self.charge:
            ## deal with windfury
            if self.windfury:
                self.remaining_attack_chance = 2
            else:
                self.remaining_attack_chance = 1

## CardState:States
    def get_name(self):
        return self.card_name

    def get_attack(self):
        return self.attack

    def get_hp(self):
        return self.current_hp

    def is_dead(self):
        return self.current_hp <= 0

    def is_taunt(self):
        return self.taunt

## CardState:Actions
    def start_turn(self):
        ## deal with windfury
        if effect1[0] == "windfury" or effect2[0] == "windfury":
            self.remaining_attack_chance = 2
        else:
            self.remaining_attack_chance = 1        

    def take_damage(self, amount):
        ## deal with divine_shield
        if self.divine_shield:
            self.divine_shield = False
            return
        else:
            self.current_hp -= amount

    def get_heal(self, amount):
        self.current_hp = min(self.current_hp + amount, self.max_hp)

    def reduce_attack_chance(self):
        self.remaining_attack_chance -= 1

    def reset_attack_chance(self):
        ## deal with windfury
        if self.windfury:
            self.remaining_attack_chance = 2
        else:
            self.remaining_attack_chance = 1

## CardState:Algorithm related methods
    def is_available_attacker(self):
        return self.remaining_attack_chance > 0 and self.attack > 0
        

#############################################################################
#############################################################################

class Mana:
    def __init__(self, initial_mana):
        self.current_mana = (initial_mana, initial_mana)
        self.max_mana = (initial_mana, initial_mana)

## Mana:States
    def get_mana(self, player):
        return self.current_mana[player], self.max_mana[player]

    def is_sufficient(self, player, card_id):
        return self.current_mana[player] >= cards[card_id][2]

## Mana:Actions
    ## at the start of once turn, his/her max_mana++
    def start_turn(self, player):
        if self.max_mana[player] < Constants.MAX_MANA_UPPER_BOUND:
            lst = list(self.max_mana)
            lst[player] += 1
            self.max_mana = tuple(lst)
        self.current_mana = deepcopy(self.max_mana)

    def add_mana(self, player, amount):
        lst = list(self.current_mana)
        lst[player] += amount
        self.current_mana = tuple(lst)
        
    def cost(self, player, amount):
        if self.current_mana[player] < amount:
            raise Exception("Insufficient mana for player %s" % player)
        lst = list(self.current_mana)
        lst[player] -= amount
        self.current_mana = tuple(lst)

    def restore(self, player, amount):
        lst = list(self.current_mana)
        lst[player] += amount
        self.current_mana = tuple(lst)

#############################################################################
#############################################################################



if __name__ == "__main__":
    game = MagicCardGame()
    game.initialize()



