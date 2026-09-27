import random

# --- Helper functions ---

def apply_damage(hp, damage):
    return max(0, hp - damage)


# TODO: Define roll_damage(min_val, max_val).
# It should return a random integer between min_val and max_val (inclusive).
def roll_damage(min_val, max_val):
    pass


def is_alive(hp):
    return hp > 0


# TODO: Define create_hero(hero_class).
# Return the matching dict below, or None if hero_class isn't one of the three.
#
# warrior → {"name": "Warrior", "hp": 120, "min_dmg": 10, "max_dmg": 20}
# mage    → {"name": "Mage",    "hp": 80,  "min_dmg": 18, "max_dmg": 28}
# rogue   → {"name": "Rogue",   "hp": 100, "min_dmg": 14, "max_dmg": 24}
def create_hero(hero_class):
    pass


# TODO: Define run_battle(hero, monster).
# Run rounds until one side's HP reaches 0. Each round, both the hero and
# the monster attack once, each dealing a random amount of damage within
# their own [min_dmg, max_dmg] range (use roll_damage and apply_damage).
# Print a line each round showing both HP totals.
#
# Return (hero["hp"], monster["hp"], round_number) once the fight ends.
def run_battle(hero, monster):
    pass


if __name__ == "__main__":
    hero_class = input("Choose your class: warrior / mage / rogue\n> ").strip().lower()
    hero = create_hero(hero_class)

    if hero is None:
        print(f"Unknown class: {hero_class!r}")
        print("Valid choices: warrior, mage, rogue")
    else:
        monster = {"name": "Goblin King", "hp": 80, "min_dmg": 8, "max_dmg": 15}

        print(f"\n{hero['name']} vs {monster['name']}!")
        print(f"Hero:  {hero['hp']} HP")
        print(f"Enemy: {monster['hp']} HP\n")

        hero_hp, monster_hp, round_number = run_battle(hero, monster)

        print()
        if is_alive(hero_hp):
            print(f"{hero['name']} wins in {round_number} rounds!")
        else:
            print(f"{hero['name']} has fallen.")
