import random

# --- Helper functions ---

def apply_damage(hp, damage):
    return max(0, hp - damage)

# TODO: Define roll_damage(min_val, max_val).
# It should return a random integer between min_val and max_val (inclusive).
def roll_damage(min_val, max_val):
    pass

# TODO: Define is_alive(hp).
# It should return True if hp > 0, False otherwise.
def is_alive(hp):
    pass

# --- Choose your hero ---

hero_class = input("Choose your class: warrior / mage / rogue\n> ").strip().lower()

hero = None

# TODO: Set hero to a dictionary based on hero_class.
#
# warrior → {"name": "Warrior", "hp": 120, "max_hp": 120, "min_dmg": 10, "max_dmg": 20}
# mage    → {"name": "Mage",    "hp": 80,  "max_hp": 80,  "min_dmg": 18, "max_dmg": 28}
# rogue   → {"name": "Rogue",   "hp": 100, "max_hp": 100, "min_dmg": 14, "max_dmg": 24}

if hero is None:
    print(f"Unknown class: {hero_class!r}")
    print("Valid choices: warrior, mage, rogue")
else:
    monster = {"name": "Goblin King", "hp": 80, "min_dmg": 8, "max_dmg": 15}

    print(f"\n{hero['name']} vs {monster['name']}!")
    print(f"Hero:  {hero['hp']} HP")
    print(f"Enemy: {monster['hp']} HP\n")

    round_number = 0

    # TODO: Write a while loop that runs as long as both sides are alive.
    # Use is_alive(hp) to check.
    #
    # Each round:
    #   1. round_number += 1
    #   2. hero_dmg = roll_damage(hero["min_dmg"], hero["max_dmg"])
    #   3. monster["hp"] = apply_damage(monster["hp"], hero_dmg)
    #   4. monster_dmg = roll_damage(monster["min_dmg"], monster["max_dmg"])
    #   5. hero["hp"] = apply_damage(hero["hp"], monster_dmg)
    #   6. Print each round:
    #      f"Round {round_number}: {hero['name']} {hero['hp']} HP | {monster['name']} {monster['hp']} HP"

    print()
    if is_alive(hero["hp"]):
        print(f"{hero['name']} wins in {round_number} rounds!")
    else:
        print(f"{hero['name']} has fallen.")
