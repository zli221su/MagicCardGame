## effect_name: (effect_id, effect_type, target_restrictions, Notes)
##               0          1            2                    3
## effect_type:   0: battlecry      1: attribute
## target_restrictions:    0: friendly target only      1: enemy target only    2: Both target are allowed   None: no Target

effects = {
    ## battlecry
    "deal_damage": (0, 0, 1, "Deal x damage to target"),
    "take_control_minion": (1, 0, 1, "Take control of an enemy minion."),
    "kill_minion": (2, 0, 1, "Kill a minion."),
    
    "heal": (3, 0, 0, "restore x hitpoint for target."),

    "transform_minion": (4, 0, 2, "Transform a minion into another minion which has car_id = x"),
    
    "aoe_heal": (5, 0, None, "restore x hitpoint for all friendly charactors."),
    "aoe": (6, 0, None, "Deal x damage to all enemies."),
    "gain_mana": (7, 0, None, "Gain x mana int this turn"),
    "draw_card": (8, 0, None, "Draw x cards"),
    "summon": (9, 0, None, "Summon another minion with car_id = x next to it"),
    "gain_mana": (10, 0, None, "Gain x mana in this turn"),
    
    "clear_board": (11, 0, None, "Destroy all minions on the board."),
    
    ## attribute
    "taunt": (20, 1, "Can attack hero when this minion is alive."),
    "divine_shield": (21, 1, "Absorb damage for one time."),
    "charge": (22, 1, "Can attack in the first round in wich it is played."),
    "windfury": (23, 1, "Can attack twice in once turn.")
}
