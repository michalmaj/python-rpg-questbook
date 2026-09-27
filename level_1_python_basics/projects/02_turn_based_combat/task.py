def fight_enemy(hero_hp, enemy_name, enemy_hp, enemy_attack, hero_attack, potions, heal_threshold=40):
    """Fight one enemy, round by round, until someone's HP reaches 0.

    `potions` is a list of heal amounts — popping one removes it from the
    hero's inventory and tells you how much HP it restores.

    Returns (hero_hp, rounds_taken, hero_won).
    """
    rounds = 0
    while hero_hp > 0 and enemy_hp > 0:
        rounds += 1

        # TODO: Hero attacks — subtract hero_attack from enemy_hp.
        #       If enemy_hp drops below 0, set it to 0.
        #       If enemy_hp == 0, the fight is over: break immediately —
        #       the enemy doesn't get to attack back this round.

        # TODO: Enemy attacks back — subtract enemy_attack from hero_hp.
        #       If hero_hp drops below 0, set it to 0.

        # TODO: If hero_hp < heal_threshold and len(potions) > 0:
        #       pop a potion, add its value to hero_hp, print a message.
        #       Otherwise: print the round status —
        #       f"  Round {rounds}: Hero HP: {hero_hp}. {enemy_name} HP: {enemy_hp}"

        # REMOVE this line once your combat logic above is complete:
        break

    return hero_hp, rounds, enemy_hp <= 0


def run_arena(hero_name, hero_hp, hero_attack, enemies, potions):
    """Send the hero through every enemy in `enemies`, in order.

    Stops early if the hero falls. Returns (final_hero_hp, battle_log).
    """
    battle_log = []
    print(f"=== {hero_name} enters the Arena ===")
    print(f"Potions: {len(potions)}")
    print()

    for enemy_name, enemy_hp, enemy_attack in enemies:
        print(f"--- {enemy_name} appears! (HP: {enemy_hp}, Attack: {enemy_attack}) ---")
        hero_hp, rounds, hero_won = fight_enemy(
            hero_hp, enemy_name, enemy_hp, enemy_attack, hero_attack, potions
        )
        if hero_won:
            print(f"{enemy_name} falls!")
            battle_log.append(f"Defeated {enemy_name} in {rounds} rounds")
        else:
            battle_log.append(f"Fell to {enemy_name}")
        print()
        if hero_hp <= 0:
            break

    print()
    if hero_hp > 0:
        print(f"{hero_name} wins the arena!")
    else:
        print(f"{hero_name} fell in the arena.")

    print()
    print("--- Battle Summary ---")
    for entry in battle_log:
        print(f"  {entry}")

    print(f"\nHero HP remaining: {hero_hp}")
    print(f"Potions remaining: {len(potions)}")

    return hero_hp, battle_log


# --- Run the arena ---
hero_name = "Ada"
hero_hp = 100
hero_attack = 20

# Arena enemies: each item is [name, hp, attack]
enemies = [
    ["Wolf", 30, 8],
    ["Orc Warrior", 55, 13],
    ["Dragon King", 90, 20],
]

# Healing potions — each value is how much HP it restores when used
potions = [30, 30, 30]

hero_hp, battle_log = run_arena(hero_name, hero_hp, hero_attack, enemies, potions)
