# Project 01: Battle Calculator
#
# Combine what you learned in Missions 01-03:
# - variables and types (Mission 01)
# - arithmetic and min/max (Mission 02)
# - input and if/elif/else (Mission 03)
#
# There are no functions here — work top to bottom.

print("=== Battle Calculator ===\n")

# --- Step 1: Choose your class ---

hero_class = input("Choose your class: warrior / mage / rogue\n> ").strip().lower()

hero_name = None
hero_hp = None
hero_damage = None
hero_gold = 50

# TODO: Set hero_name, hero_hp, and hero_damage based on hero_class.
#
# warrior → hero_name = "Warrior", hero_hp = 120, hero_damage = 15
# mage    → hero_name = "Mage",    hero_hp = 80,  hero_damage = 25
# rogue   → hero_name = "Rogue",   hero_hp = 100, hero_damage = 20

if hero_name is None:
    print(f"\nUnknown class: {hero_class!r}")
    print("Valid choices: warrior, mage, rogue")
else:
    max_hp = hero_hp

    print(f"\n{hero_name} enters the arena!")
    print(f"HP: {hero_hp}  |  Damage: {hero_damage}  |  Gold: {hero_gold}\n")

    # --- Step 2: Monster attacks ---

    monster_damage = 20

    # TODO: Calculate hero_hp after taking monster_damage. HP cannot go below 0.
    # Hint: max(0, value)
    hero_hp = None

    print(f"The monster deals {monster_damage} damage!")
    print(f"Your HP: {hero_hp}")

    # --- Step 3: Use a potion? ---

    use_potion = input("\nUse a potion? (yes/no)\n> ").strip().lower()

    if use_potion == "yes":
        potion_heal = 25
        # TODO: Calculate hero_hp after healing. HP cannot exceed max_hp.
        # Hint: min(max_hp, value)
        hero_hp = None
        print(f"You healed! HP: {hero_hp}")

    # --- Step 4: Battle summary ---

    print("\n=== Battle Summary ===")
    # TODO: If hero_hp > 0, print: f"{hero_name} stands with {hero_hp} HP remaining."
    #       Otherwise, print: f"{hero_name} has fallen."
