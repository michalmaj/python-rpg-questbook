# Mission 02: Damage and Healing
#
# The hero starts with 100 HP.
# Use arithmetic to track HP through three events.

hero_hp = 100
max_hp = 100
monster_damage = 30
potion_heal = 20
big_hit = 200

# TODO: Hero takes monster_damage. HP cannot go below 0.
# Hint: max(0, value)
hp_after_attack = None

# TODO: Hero drinks a potion. HP cannot exceed max_hp.
# Hint: min(max_hp, value)
hp_after_healing = None

# TODO: Hero takes big_hit damage. HP cannot go below 0.
hp_after_big_hit = None

print("=== HP Log ===")
print(f"Starting HP:    {hero_hp}")
print(f"After attack:   {hp_after_attack}")
print(f"After healing:  {hp_after_healing}")
print(f"After big hit:  {hp_after_big_hit}")
