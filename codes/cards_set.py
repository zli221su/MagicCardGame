from effects_set import effects

## card_id: (card_name, card_type, card_cost, target_type, attack, hitpoint, effect1, effect1_amount, effect2, effect2_amount, Notes)
##            0          1          2          3           4       5         6         7              8        9               10
## card_type:     0: spell       1: minion
## target_type:   0: hero only   1: minion only   2: any enemy

cards = {
    0: ("Coin", 0, 0, None, None, None, "gain_mana", 1, None, None, "Gain 1 mana in this turn."),
    1: ("Innervate", 0, 0, None, None, None, "gain_mana", 2, None, None, "Gain 2 mana in this turn."),
    2: ("Moonfire", 0, 0, 2, None, None, "deal_damage", 1, None, None, "Deal 1 damage."),
    4: ("Wisp", 1, 0, None, 1, 1, None, None, None, None, "Void."),
    5: ("Target Dummy", 1, 0, None, 0, 2, "taunt", None, None, None, "Void."),
    93: ("Frog", 1, 0, None, 0, 1, "taunt", None, None, None, "A frog made by 'Hex'."),

    
    6: ("Argent Squire", 1, 1, None, 1, 1, "divine_shield", None, None, None, "Void."),
    7: ("Elven Archer", 1, 1, 2, 1, 1, "deal_damage", 1, None, None, "Deal 1 damage to target."),
    8: ("Goldshire Footman", 1, 1, None, 1, 2, "taunt", None, None, None, "Void."),
    9: ("Murioc Raider", 1, 1, None, 2, 1, None, None, None, None, "Void."),
    10: ("Stonetusk Boar", 1, 1, None, 1, 1, "charge", None, None, None, "Void."),
    80: ("Holy Smite", 0, 1, 2, None, None, "deal_damage", 2, None, None, "Deal 2 damage to target."),
    81: ("Power Word: Shield", 0, 1, 1, None, None, "heal", 3, "draw_card", 1, "Restore 3 health for a minion and draw 1 card."),
    85: ("Sinister Strike", 0, 1, 0, None, None, "deal_damage", 3, None, None, "Deal 3 damage to target hero."),
    91: ("Frost Shock", 0, 1, 2, None, None, "deal_damage", 2, None, None, "Deal 2 damage to target."),
    108: ("Righteous Protector", 1, 1, None, 1, 1, "taunt", None, "divine_shield", None, "Void."),
    116: ("Pit Snake", 1, 1, None, 2, 1, None, None, None, None, "Void."),
    118: ("Defias Theif", 1, 1, None, 2, 1, None, None, None, None, "Created by 'Defias Ringleader'."),
    120: ("Warbot", 1, 1, None, 1, 3, None, None, None, None, "Void."),
    126: ("Flash Heal", 0, 1, 2, None, None, "heal", 5, None, None, "Restore 5 health for target."),
    129: ("Young Dragonhawk", 1, 1, None, 1, 1, "windfury", None, None, None, "Void."),
    
    
    3: ("Wrath1", 0, 2, 1, None, None, "deal_damage", 1, "draw_card", 1, "Deal 1 damage and draw 1 card."),
    11: ("Annoy-o-Tron", 1, 2, None, 1, 2, "taunt", None, "divine_shield", None, "Void."),
    12: ("Bloodfen Raptor", 1, 2, None, 3, 2, None, None, None, None, "Void."),
    13: ("Bluegill Warrior", 1, 2, None, 2, 1, "charge", None, None, None, "Void."),
    14: ("Duskboar", 1, 2, None, 4, 1, None, None, None, None, "Void."),
    15: ("pompous Thespian", 1, 2, None, 3, 2, "taunt", None, None, None, "Void."),
    16: ("Novice Engineer", 1, 2, None, 1, 2, "draw_card", 1, None, None, "Draw 1 card."),
    17: ("River Crocolisk", 1, 2, None, 2, 3, None, None, None, None, "Void."),
    71: ("Arcane Explosion", 0, 2, None, None, None, "aoe", 1, None, None, "Deal 1 damage to all enemy minions."),
    72: ("Frostbolt", 0, 2, 2, None, None, "deal_damage", 3, None, None, "Deal 2 damage to target."),
    78: ("Holy Light", 0 ,2, 2, None, None, "heal", 6, None, None, "Restore 6 health for target."),
    82: ("Mind Blast", 0, 2, 0, None, None, "deal_damage", 5, None, None, "Deal 5 damage to target hero."),
    86: ("Eviscerate", 0, 2, 2, None, None, "deal_damage", 4, None, None, "Deal 4 damage to target."),
    87: ("Shiv", 0, 2, 2, None, None, "deal_damage", 1, "draw_card", 1, "Deal 1 damage to target and draw 1 card"),
    105: ("Treants", 1, 2, None, 2, 2, "taunt", None, None, None, "Created by 'Cenarius'."),
    106: ("Sorcerer's Apprentce", 1, 2, None, 3, 2, None, None, None, None, "Void."),
    109: ("Shielded Minibot", 1, 2, None, 2, 2, "taunt", None, "divine_shield", None, "Void."),
    117: ("Defias Ringleader", 1, 2, None, 2, 2, "summon", 118, None, None, "Summons 1 2/1 minion."), ## summon 118
    127: ("Darkbomb", 0, 2, 2, None, None, "deal_damage", 3, None, None, "Deal 3 damage to target."),
    128: ("Whirling Zap-o-matic", 1, 2, None, 3, 2, "windfury", None, None, None, "Void."),
    
    
    18: ("Am'gam Rager", 1, 3, None, 1, 5, None, None, None, None, "Void."),
    19: ("Argent Horserider", 1, 3, None, 2, 1, "charge", None, "divine_shield", None, "Void."),
    20: ("Disciple of CThun", 1, 3, 2, 2, 1, "deal_damage", 2, None, None, "Deals 2 damage to target."),
    21: ("Earthen Ring Farseer", 1, 3, 2, 3, 3, "heal", 3, None, None, "Restore 3 health."), 
    22: ("Gnomeregan infantry", 1, 3, None, 1, 4, "charge", None, "taunt", None, "Void."),
    23: ("Hired Gun", 1, 3, None, 4, 3, "taunt", None, None, None, "Void."),
    24: ("Ice Rager", 1, 3, None, 5, 2, None, None, None, None, "Void."),
    25: ("Ironforge Rifleman", 1, 3, 2, 2, 2, "deal_damage", 1, None, None, "Deal 1 damage to target."),
    26: ("Razorfen Hunter", 1, 3, None, 2, 3, "summon", 6, None, None, "Void."), ## pay attention to this summon card_id = 6
    27: ("Scarlet Crusader", 1, 3, None, 3, 1, "divine_shield", None, None, None, "Void."),
    28: ("Spider Tank", 1, 3, None, 3, 4, None, None, None, None, "Void."),
    29: ("Wolfrider", 1, 3, None, 3, 1, "charge", None, None, None, "Void."),
    73: ("Arcane Intellect", 0, 3, None, None, None, "draw_card", 2, None, None, "Draw 2 cards."),
    88: ("Fan of Knives", 0, 3, None, None, None, "aoe", 1, "draw_card", 1, "Deal 1 damage to enemy minions and draw 1 card."),
    94: ("Shadow Bolt", 0, 3, 1, None, None, "deal_damage", 4, None, None, "Deal 4 damage to target minion."),
    96: ("Shield Block", 0, 3, 0, None, None, "heal", 5, "draw_card", 1, "Restore 5 health for target hero and draw 1 card."),
    97: ("Healing Touvh", 0, 3, 2, None, None, "heal", 8, None, None, "Restore 8 health for target."),
    107: ("Twilight Flamecaller", 1, 3, None, 2, 2, "aoe", 1, None, None, "Deal 1 damage to all enemy minions."),
    110: ("Benevolent Djinn", 1, 3, 0, 2, 4, "heal", 3, None, None, "Restore 3 health for target hero."),
    112: ("Dummy Uldaman", 1, 3, None, 3, 3, None, None, None, None, "Created by 'Keeper of Uldaman'."),
    121: ("Fierce Monkey", 1, 3, None, 3, 4, "taunt", None, None, None, "Void."),
    122: ("Rabid Worgen", 1, 3, None, 3, 1, "charge", None, None, None, "Void."),
    130: ("Flying Machine", 1, 3, None, 1, 4, "windfury", None, None, None, "Void."),
    131: ("Thrallmar Farseer", 1, 3, None, 2, 3, "windfury", None, None, None, "Void."),


    30: ("Chillwind Yeti", 1, 4, None, 4, 5, None, None, None, None, "Void."),
    31: ("Dragonling Mechanic", 1, 4, None, 2, 4, "summon", 9, None, None, "Summon a 2/1 minion."), ## summon 9
    32: ("Evil Heckler", 1, 4, None, 5, 4, None, None, None, None, "Void."),
    33: ("Gnomish inventor", 1, 4, None, 2, 4, "draw_card", 1, None, None, "Draw a card."),
    34: ("Fire Plume Phoenix", 1, 4, 2, 3, 3, "deal_damage", 2, None, None, "Deal 2 damage to target."),
    35: ("Grim Necromancer", 1, 4, None, 2, 4, "summon", 9, "summon", 9, "Summon 2 1/1 minions."), ## summon 9 * 2
    36: ("Lost Tallstrider", 1, 4, None, 5, 4, None, None, None, None, "Void."),
    37: ("Mogu'shan Warden", 1, 4, None, 1, 7, "taunt", None, None, None, "Void."),
    38: ("Oasis Snapjaw", 1, 4, None, 2, 7, None, None, None, None, "Void."),
    39: ("Sen'jin Shieldmasta", 1, 4, None, 3, 5, "taunt", None, None, None, "Void."),
    40: ("Worgen Greaser", 1, 4, None, 6, 3, None, None, None, None, "Void."),
    74: ("Fireball", 0, 4, 2, None, None, "deal_damage", 6, None, None, "Deal 6 damage to target"),
    75: ("Polymorph", 0, 4, 1, None, None, "transform_minion", 6, None, None, "Transform a minion into a 1/1 Argent Squire"), ## transform_minion 6
    79: ("Consecration", 0, 4, None, None, None, "aoe", 2, None, None, "Deal 2 damage to all enemies."),
    92: ("Hex", 0, 4, 1, None, None, "transform_minion", 93, None, None, "Transform a minion into a 0/1 frog."), ## transform 93
    99: ("Keeper of the Grove", 1, 4, 2, 2, 4, "deal_damage", 2, None, None, "Deal 2 damage to target."),
    111: ("Keeper of Uldaman", 1, 4, 1, 3, 3, "transform_minion", 112, None, None, "Transform target minion into a 3/3 minion."), ## transform 112
    114: ("Shifting Shade", 1, 4, None, 4, 3, None, None, None, None, "Void."),
    119: ("Tomb Pillager", 1, 4, None, 4, 3, "gain_mana", 1, None, None, "Gain 1 mana."),
    123: ("Lor'kron Elite", 1, 4, None, 4, 3, "charge", None, None, None, "Void."),

    
    41: ("Antique Healbot", 1, 5, 0, 3, 3, "heal", 8, None, None, "Restore 8 health for target hero."),
    42: ("Azure Drake", 1, 5, None, 4, 5, "draw_card", 1, None, None, "Draw a card."),
    43: ("Booty Bay Bodyguard", 1, 5, None, 5, 4, None, None, None, None, "Void."),
    44: ("Blackwing Corruptor", 1, 5, 2, 5, 4, "deal_damage", 3, None, None, "Deal 2 damage to target."),
    45: ("Darkscale Healer", 1, 5, None, 4, 5, "aoe_heal", 2, None, None, "Restore 2 health for all friendly minions."),
    46: ("Fen Creeper", 1, 5, None, 3, 6, "taunt", None, None, None, "Void."),
    47: ("Nightblade", 1, 5, 0, 4, 4, "deal_damage", 3, None, None, "Deal 3 damage to target hero."),
    48: ("Pit Fighter", 1, 5, None, 5, 6, None, None, None, None, "Void."),
    49: ("Psych-o-Tron", 1, 5, None, 3, 4, "taunt", None, "divine_shield", None, "Void."),
    50: ("Salty Dog", 1, 5, None, 7, 4, None, None, None, None, "Void."),
    51: ("Stormpike Commando", 1, 5, 2, 4, 2, "deal_damage", 2, None, None, "Deal 2 damage to target."),
    83: ("Holy Nova", 0, 5, None, None, None, "aoe", 2, "aoe_heal", 2, "Deal 2 damage to all enemy minions and restore 2 health to friendly minions."),
    89: ("Assassinate", 0, 5, 1, None, None, "kill_minion", None, None, None, "Destroy target minion."),
    100: ("Druid of the Claw", 1, 5, None, 4, 6, "taunt", None, None, None, "Void."),
    115: ("Darkshire Alchemist", 1, 5, 2, 4, 5, "heal", 5, None, None, "Restore 5 health for target."),
    132: ("Grook Fu Master", 1, 5, None, 3, 5, "windfury", None, None, None, "Void."),
    
    
    52: ("Ancient of Blossoms", 1, 6, None, 3, 8, "taunt", None, None, None, "Void."),
    53: ("Argent Commander", 1, 6, None, 4, 2, "charge", None, "divine_shield", None, "Void."),
    54: ("Boulderfist Ogre", 1, 6, None, 6, 7, None, None, None, None, "Void."),
    55: ("Lord of the Arena", 1, 6, None, 6, 5, "taunt", None, None, None, "Void."),
    56: ("Priestess of Elune", 1, 6, 0, 5, 4, "heal", 4, None, None, "Void."),
    57: ("Reckless Rocketeer", 1, 6, None, 5, 2, "charge", None, None, None, "Void."),
    58: ("Sunwlker", 1, 6, None, 4, 5, "taunt", None, "divine_shield", None, "Void."),
    98: ("Starfire", 0, 6, 2, None, None, "deal_damage", 5, "draw_card", 1, "Deal 5 damage to target and draw 1 card."),
    133: ("Windfury Harpy", 1, 6, None, 4, 5, "windfury", None, None, None, "Void."),

    
    90: ("Sprint", 0, 7, None, None, None, "draw_card", 4, None, None, "Draw 4 cards."),
    59: ("Bog Creeper", 1, 7, None, 6, 8, "taunt", None, None, None, "Void."),
    60: ("Captured Jormungar", 1, 7, None, 5, 9, None, None, None, None, "Void."),
    61: ("Core Hound", 1, 7, None, 9, 5, None, None, None, None, "Void."),
    62: ("War Golem", 1, 7, None, 7, 7, None, None, None, None, "Void."),
    76: ("Fiamestrike", 0, 7, None, None, None, "aoe", 4, None, None, "Deal 4 damage to all enemy minions."),
    101: ("Ancient of Lore", 1, 7, None, 5, 5, "draw_card", 2, None, None, "Void."),
    102: ("Ancient of War", 1, 7, None, 10, 5, None, None, None, None, "Void."),
    113: ("Guardian of Kings", 1, 7, 0, 5, 6, "heal", 6, None, None, "Restore 6 health for target hero."),
    134: ("Grotesque Dragonhawk", 1, 7, None, 5, 5, "windfury", None, None, None, "Void."),
    63: ("Eldritch Horror", 1, 8, None, 6, 10, None, None, None, None, "Void."),
    64: ("Force-Tank MAX", 1, 8, None, 7, 7, "divine_shield", None, None, None, "Void."),
    65: ("Fossilized Devilsaur", 1, 8, None, 8, 8, "taunt", None, None, None, "Void."),
    77: ("Pyroblast", 0, 8, 2, None, None, "deal_damage", 10, None, None, "Deal 10 damage to target."),
    84: ("Mind Control", 0, 8, 1, None, None, "take_control_minion", None, None, None, "Take control of target minion"),
    95: ("Twisting Nether", 0, 8, None, None, None, "clear_board", None, None, None, "Destroy all minions."),
    103: ("Ironbark Protector", 1, 8, None, 8, 8, "taunt", None, None, None, "Void."),
    125: ("Lay on Hands", 0, 8, 2, None, None, "heal", 8, "draw_card", 3, "Restore 8 health for target and draw 3 cards."),
    66: ("Bull Dozer", 1, 9, None, 9, 7, "divine_shield", None, None, None, "Void."),
    67: ("North Sea Kraken", 1, 9, 2, 9, 7, "deal_damage", 4, None, None, "Void."),
    68: ("Sleepy Dragon", 1, 9, None, 4, 12, "taunt", None, None, None, "Void."),
    104: ("Cenarius", 1, 9, None, 5, 8, "summon", 105, None, None, "Summon 2 2/2minions with taunt."),
    69: ("Faceless Bechemoth", 1, 10, None, 10, 10, None, None, None, None, "Void."),
    70: ("Ultrasaur", 1, 10, None, 7, 14, None, None, None, None, "Void."),
    124: ("Varian Wrynn", 1, 10, None, 7, 7, "draw_card", 4, None, None, "Void.")

}

class CardClassify:
    def __init__(self):
        self.cost_0 = []
        self.cost_1 = []
        self.cost_2 = []
        self.cost_3 = []
        self.cost_4 = []
        self.cost_5 = []
        self.cost_6 = []
        self.cost_7p = []
        self.initialize()

    def initialize(self):
        for i in cards:
            cost = cards[i][2]
            if cost == 0:
                self.cost_0.append(i)
            elif cost == 1:
                self.cost_1.append(i)
            elif cost == 2:
                self.cost_2.append(i)
            elif cost == 3:
                self.cost_3.append(i)
            elif cost == 4:
                self.cost_4.append(i)
            elif cost == 5:
                self.cost_5.append(i)
            elif cost == 6:
                self.cost_6.append(i)
            elif cost >= 7:
                self.cost_7p.append(i)
            else:
                raise Exception("Wrong cost with Card_id = %s" % i)

if __name__ == "__main__":
    for i in range(len(cards)):
        print("card_id = %s  " % i, end = "")
        if cards[i][6] is not None:
            print("%s  %s" % (effects[cards[i][6]], cards[i][7]), end = "")
        print("")
