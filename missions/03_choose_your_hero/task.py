def choose_hero_class(choice: str) -> dict | None:
    # TODO: Return a dict for each valid class name:
    #
    # "warrior" → {"class": "Warrior", "hp": 120, "damage": 15, "bonus": "armor"}
    # "mage"    → {"class": "Mage",    "hp": 80,  "damage": 25, "bonus": "spell"}
    # "rogue"   → {"class": "Rogue",   "hp": 100, "damage": 20, "bonus": "crit"}
    #
    # If choice is not one of the above, return None.
    pass


if __name__ == "__main__":
    print("Choose your class: warrior / mage / rogue")
    choice = input("> ").strip().lower()

    hero = choose_hero_class(choice)

    if hero:
        print(f"\nYou chose: {hero['class']}")
        print(f"HP:     {hero['hp']}")
        print(f"Damage: {hero['damage']}")
        print(f"Bonus:  {hero['bonus']}")
    else:
        print(f"\nUnknown class: {choice!r}")
        print("Valid choices: warrior, mage, rogue")
