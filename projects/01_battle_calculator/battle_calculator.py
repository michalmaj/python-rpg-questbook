"""Project 01: Battle Calculator

Combine what you learned in Missions 01-03 to build a small battle simulator.
Each function below should feel familiar — you wrote similar logic in the missions.
"""


def get_hero_stats(hero_class: str) -> dict | None:
    # TODO: Return stats for the chosen hero class, or None if unknown.
    #
    # "warrior" → {"class": "Warrior", "hp": 120, "damage": 15, "gold": 50}
    # "mage"    → {"class": "Mage",    "hp": 80,  "damage": 25, "gold": 50}
    # "rogue"   → {"class": "Rogue",   "hp": 100, "damage": 20, "gold": 50}
    pass


def calculate_damage(hero_hp: int, damage: int) -> int:
    # TODO: Subtract damage from hero_hp. HP cannot go below 0.
    pass


def calculate_healing(hero_hp: int, heal_amount: int, max_hp: int) -> int:
    # TODO: Add heal_amount to hero_hp. HP cannot exceed max_hp.
    pass


def summarize_battle(hero_class: str, final_hp: int) -> str:
    # TODO: Return a summary string.
    # If final_hp > 0:  "Warrior stands with 65 HP remaining."
    # If final_hp == 0: "Mage has fallen."
    pass


if __name__ == "__main__":
    print("=== Battle Calculator ===\n")
    print("Choose your class: warrior / mage / rogue")
    choice = input("> ").strip().lower()

    hero = get_hero_stats(choice)
    if not hero:
        print(f"Unknown class: {choice!r}")
    else:
        max_hp = hero["hp"]
        current_hp = max_hp
        print(f"\n{hero['class']} steps into the arena!")
        print(f"HP: {current_hp}  |  Damage: {hero['damage']}\n")

        try:
            damage_input = input("Monster attacks! How much damage? ").strip()
            damage = int(damage_input)
        except ValueError:
            print("That's not a number. Defaulting to 20 damage.")
            damage = 20

        current_hp = calculate_damage(current_hp, damage)
        print(f"After {damage} damage: {current_hp} HP")

        heal_input = input("Use a potion? (yes/no) ").strip().lower()
        if heal_input == "yes":
            current_hp = calculate_healing(current_hp, 25, max_hp)
            print(f"After healing: {current_hp} HP")

        print()
        print(summarize_battle(hero["class"], current_hp))
