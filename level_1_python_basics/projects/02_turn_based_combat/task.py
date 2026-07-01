hero_name = "Ada"
hero_hp = 100
hero_attack = 20

# Arena enemies: each item is [name, hp, attack]
enemies = [
    ["Wolf",        30,  8],
    ["Orc Warrior", 55, 13],
    ["Dragon King", 90, 20],
]

# Healing potions — each restores this many HP when used
potions = [30, 30, 30]

# Record of each battle outcome (append strings here during combat)
battle_log = []

print(f"=== {hero_name} enters the Arena ===")
print(f"Potions: {len(potions)}")
print()

for enemy in enemies:
    enemy_name   = enemy[0]
    enemy_hp     = enemy[1]
    enemy_attack = enemy[2]

    print(f"--- {enemy_name} appears! (HP: {enemy_hp}, Attack: {enemy_attack}) ---")

    round_num = 0
    while hero_hp > 0 and enemy_hp > 0:
        round_num += 1

        # TODO: Hero attacks — subtract hero_attack from enemy_hp.
        #       If enemy_hp drops below 0, set it to 0.
        #       If enemy_hp == 0: print the defeat message, append to battle_log, break.

        # TODO: Enemy attacks back — subtract enemy_attack from hero_hp.
        #       If hero_hp drops below 0, set it to 0.

        # TODO: If hero_hp < 40 and len(potions) > 0:
        #       call potions.pop() to remove the last potion,
        #       add the heal to hero_hp, and print the potion message.
        #       Otherwise: print the round status (hero HP, enemy HP).

        # REMOVE this line once your combat logic above is complete:
        break

    # If the hero was defeated inside the while loop, stop the arena
    if hero_hp <= 0:
        battle_log.append(f"Fell to {enemy_name}")
        break

    print()

print()
# TODO: Print win or loss message.
#       If hero_hp > 0: print("{hero_name} wins the arena!")
#       Else:           print("{hero_name} fell in the arena.")

print()
print("--- Battle Summary ---")
# TODO: Loop over battle_log and print each entry with two leading spaces.

print(f"\nHero HP remaining: {hero_hp}")
print(f"Potions remaining: {len(potions)}")
