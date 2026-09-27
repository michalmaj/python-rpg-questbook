from dataclasses import dataclass
import csv
import json

from combat import apply_damage, is_alive, roll_damage


@dataclass
class Hero:
    name: str
    hero_class: str
    hp: int
    max_hp: int
    damage_min: int
    damage_max: int


hero_name = input("Enter your hero's name: ")

# TODO 1: Create your Hero — pick ONE class and use its matching stats.
#
# Warrior: hp=120, max_hp=120, damage_min=10, damage_max=20
# Mage:    hp=80,  max_hp=80,  damage_min=18, damage_max=28
# Rogue:   hp=100, max_hp=100, damage_min=14, damage_max=24
hero = None

# Boss stats (given — don't change)
boss_name = "Shadow Dragon"
boss_hp = 150
boss_damage_min = 12
boss_damage_max = 20

combat_log = []
round_number = 0

print(f"\n{hero.name} the {hero.hero_class} faces the {boss_name}!")
print("-" * 40)

# TODO 2: Write the combat loop.
#
# While both the hero and the boss are alive:
#   - increase round_number
#   - the hero deals roll_damage(hero.damage_min, hero.damage_max) to boss_hp
#   - if the boss is still alive, it deals roll_damage(boss_damage_min, boss_damage_max)
#     back to hero.hp — a dead boss does not attack
#   - append [round_number, hero.hp, boss_hp] to combat_log
#   - print a line showing the round's damage and both HP totals

# TODO 3: Print the result — who won.

# TODO 4: Save the hero's final state to save_game.json.
# Must include at least: name, class, hp, max_hp.

# TODO 5: Write combat_log to combat_log.csv.
# Header row: round,hero_hp,boss_hp — one data row per round.
