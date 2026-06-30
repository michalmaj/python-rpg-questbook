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

# TODO 1: Create your Hero — uncomment ONE of the three lines below.
#
# Warrior: high HP, moderate damage
# hero = Hero(name=hero_name, hero_class="Warrior", hp=120, max_hp=120, damage_min=10, damage_max=20)
#
# Mage: low HP, high damage
# hero = Hero(name=hero_name, hero_class="Mage", hp=80, max_hp=80, damage_min=18, damage_max=28)
#
# Rogue: medium HP, medium-high damage
# hero = Hero(name=hero_name, hero_class="Rogue", hp=100, max_hp=100, damage_min=14, damage_max=24)

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
# Both hero and boss attack each round. The boss only attacks if it is still alive.
# Append [round_number, hero.hp, boss_hp] to combat_log each round.
# Print a summary line each round.
#
# while is_alive(hero.hp) and is_alive(boss_hp):
#     round_number += 1
#     hero_dmg = roll_damage(hero.damage_min, hero.damage_max)
#     boss_hp = apply_damage(boss_hp, hero_dmg)
#     boss_dmg = 0
#     if is_alive(boss_hp):
#         boss_dmg = roll_damage(boss_damage_min, boss_damage_max)
#         hero.hp = apply_damage(hero.hp, boss_dmg)
#     combat_log.append([round_number, hero.hp, boss_hp])
#     print(f"Round {round_number}: {hero.name} deals {hero_dmg} | {boss_name} deals {boss_dmg} | Hero HP: {hero.hp} | Boss HP: {boss_hp}")

# TODO 3: Print the result.
# if is_alive(hero.hp):
#     print(f"\n{hero.name} wins! The {boss_name} is defeated.")
# else:
#     print(f"\n{hero.name} has fallen. The {boss_name} prevails.")

# TODO 4: Save the hero's final state to save_game.json.
# with open("save_game.json", "w") as f:
#     json.dump(
#         {"name": hero.name, "class": hero.hero_class, "hp": hero.hp, "max_hp": hero.max_hp},
#         f,
#         indent=2,
#     )

# TODO 5: Write the combat log to combat_log.csv.
# with open("combat_log.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(["round", "hero_hp", "boss_hp"])
#     writer.writerows(combat_log)
