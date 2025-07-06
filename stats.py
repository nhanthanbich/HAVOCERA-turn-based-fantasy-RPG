import random as rd

species_base_stats = {
    "Witch": {
        "role": "Pháp sư, Cấu rỉa", "strength": 41, "stamina": 177,
        "vitality": 711, "dexterity": 44, "agility": 15
    },
    "Vampire": {
        "role": "Pháp sư", "strength": 67, "stamina": 54,
        "vitality": 1455, "dexterity": 10, "agility": 20
    },
    "Werewolf": {
        "role": "Sát thủ", "strength": 98, "stamina": 34,
        "vitality": 819, "dexterity": 45, "agility": 29
    },
}

def compute_combat_stats(info):
    return {
        "atk": info["strength"],
        "hp": info["vitality"],
        "crit": info["dexterity"],
        "dodge": info["agility"]
    }

def rand_stat(attr, base):
    if attr == "vitality":
        delta = 115
    elif attr in ["dexterity", "agility"]:
        delta = 5
    else:
        delta = 15
    return max(0, base + rd.randint(-delta, delta))
