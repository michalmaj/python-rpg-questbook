# Mission 04: Combat Loop

hero_hp = 100
hero_damage = 15

monster_name = "Goblin"
monster_hp = 60
monster_damage = 12

round_number = 0

print("=== Battle Begins! ===")
print(f"Hero:    {hero_hp} HP")
print(f"{monster_name}: {monster_hp} HP")
print()

# TODO: Write a while loop that runs as long as hero_hp > 0 AND monster_hp > 0.
#
# Each round should:
#   1. Add 1 to round_number
#   2. Subtract hero_damage from monster_hp  — use max(0, monster_hp - hero_damage)
#   3. Subtract monster_damage from hero_hp  — use max(0, hero_hp - monster_damage)
#   4. Print the round result:
#      print(f"Round {round_number}: Hero {hero_hp} HP | {monster_name} {monster_hp} HP")

print("=== Battle Over ===")
# TODO: If hero_hp > 0, print f"Hero wins in {round_number} rounds!"
#       Otherwise, print f"{monster_name} wins in {round_number} rounds!"
