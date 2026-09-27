# Mission 19: Party Damage Grid

import numpy as np

# Damage dealt by each hero, round by round.
#
#           Round 1  Round 2  Round 3  Round 4
# Warrior      12       15       10       18
# Mage         20        5       22       19
# Rogue        14       14       16       15
damage = np.array([
    [12, 15, 10, 18],
    [20, 5, 22, 19],
    [14, 14, 16, 15],
])

# TODO: How many heroes and how many rounds does this grid hold?
# Expected: (3, 4)
grid_shape = None

# TODO: Get the Warrior's damage across all four rounds — the first row.
# Expected: [12 15 10 18]
warrior_damage = None

# TODO: Get everyone's damage in Round 2 — the second column.
# Expected: [15  5 14]
round_2_damage = None

# TODO: Total damage each hero dealt across every round. One number per
# hero — the round dimension collapses, the hero dimension survives.
# Expected: [55 66 59]
damage_per_hero = None

# TODO: Total damage the whole party dealt in each round. One number per
# round — the hero dimension collapses this time, the round dimension survives.
# Expected: [46 34 48 52]
damage_per_round = None

# TODO: The party drinks a power potion — +2 damage on every single hit,
# every hero, every round, in one operation. Shape stays (3, 4).
buffed_damage = None

print(f"grid_shape:       {grid_shape}")
print(f"warrior_damage:   {warrior_damage}")
print(f"round_2_damage:   {round_2_damage}")
print(f"damage_per_hero:  {damage_per_hero}")
print(f"damage_per_round: {damage_per_round}")
print(f"buffed_damage:\n{buffed_damage}")
