# Mission 05: Arena Challenge

rounds = 5
hero_hp = 100
hero_damage = 15

enemy_name = "Stone Golem"
enemy_hp = 200
enemy_damage = 12

print(f"=== Arena Challenge: {rounds} Rounds ===")
print(f"Hero:         {hero_hp} HP")
print(f"{enemy_name}: {enemy_hp} HP")
print()

# TODO: Use a for loop to run exactly `rounds` rounds.
# Hint: for round_number in range(1, rounds + 1):
#
# Each round:
#   1. Subtract hero_damage from enemy_hp   — use max(0, enemy_hp - hero_damage)
#   2. Subtract enemy_damage from hero_hp   — use max(0, hero_hp - enemy_damage)
#   3. Print: f"Round {round_number}: Hero {hero_hp} HP | {enemy_name} {enemy_hp} HP"

print()
print("=== Time is up! ===")
# TODO: If hero_hp > 0, print f"Hero survives with {hero_hp} HP!"
#       Otherwise, print "Hero has fallen."
