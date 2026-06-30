# Mission 03: Choose Your Hero

hero_class = input("Choose your class: warrior / mage / rogue\n> ").strip().lower()

hero_name = None
hero_hp = None
hero_damage = None
hero_bonus = None

# TODO: Use if / elif / elif / else to set hero_name, hero_hp, hero_damage, and hero_bonus.
#
# warrior → hero_name = "Warrior", hero_hp = 120, hero_damage = 15, hero_bonus = "armor"
# mage    → hero_name = "Mage",    hero_hp = 80,  hero_damage = 25, hero_bonus = "spell"
# rogue   → hero_name = "Rogue",   hero_hp = 100, hero_damage = 20, hero_bonus = "crit"

if hero_name is not None:
    print(f"\nYou chose: {hero_name}")
    print(f"HP:     {hero_hp}")
    print(f"Damage: {hero_damage}")
    print(f"Bonus:  {hero_bonus}")
else:
    print(f"\nUnknown class: {hero_class!r}")
    print("Valid choices: warrior, mage, rogue")
