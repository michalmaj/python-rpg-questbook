# Mission 18: Critical Hits

import numpy as np

# --- Part 1: which rolls were critical? ---
#
# Eight attack rolls from the last fight. A roll of 6 is a critical hit.
attack_rolls = np.array([3, 6, 1, 6, 4, 2, 6, 5])

# TODO: Build a boolean array — one True/False per roll — that is True
# wherever a roll equals 6. Comparing an array to a value with == does
# this for every element at once.
is_critical = None

# TODO: Use is_critical to select only the critical rolls from attack_rolls.
# A boolean array can index another array directly: arr[mask].
critical_rolls = None

# TODO: How many rolls were critical? True counts as 1 when summed.
critical_count = None

print("=== Critical Hits ===")
print(f"attack_rolls:   {attack_rolls}")
print(f"is_critical:    {is_critical}")
print(f"critical_rolls: {critical_rolls}")
print(f"critical_count: {critical_count}")

# --- Part 2: which hits dealt high damage? ---
#
# Damage dealt by each of the same eight attacks. A hit counts as
# "high damage" if it dealt more than 20 damage.
damage_dealt = np.array([12, 25, 4, 22, 15, 8, 28, 18])

# TODO: Same three steps as Part 1 — build the mask, select the matching
# values, then count them. Different array, different condition.
is_high_damage = None
high_damage_hits = None
high_damage_count = None

print()
print("=== High Damage Hits ===")
print(f"damage_dealt:      {damage_dealt}")
print(f"is_high_damage:    {is_high_damage}")
print(f"high_damage_hits:  {high_damage_hits}")
print(f"high_damage_count: {high_damage_count}")
