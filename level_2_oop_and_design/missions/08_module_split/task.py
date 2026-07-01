# Mission 08: Module Split
#
# The rpg/ package contains four modules.
# hero.py and monster.py are provided and complete.
# Your job: fill in the TODOs in rpg/combat.py, then run this file.
#
# Open rpg/combat.py and implement:
#   compute_damage(atk, def_) -> int
#   hero_turn(hero, monster)  -> tuple[int, bool]
#   monster_turn(monster, hero) -> tuple[int, bool]


from rpg.hero import Hero, HeroClass
from rpg.monster import Monster, MONSTER_TEMPLATES


if __name__ == "__main__":
    import random
    from rpg.combat import hero_turn, monster_turn

    hero = Hero(
        name="Ada",
        hero_class=HeroClass.WARRIOR,
        hp=120, max_hp=120, atk=15, def_=8,
        potions=2, gold=20,
    )
    template = random.choice(MONSTER_TEMPLATES)
    monster  = Monster(template)

    print(f"{hero} vs {monster}\n")

    for turn in range(1, 4):
        if not hero.is_alive or not monster.is_alive:
            break
        dmg, crit = hero_turn(hero, monster)
        label = "CRITICAL! " if crit else ""
        print(f"Turn {turn}: {label}{hero.name} deals {dmg} → {monster.name} HP={monster.hp}")

        if not monster.is_alive:
            print(f"{monster.name} defeated!")
            break

        dmg, crit = monster_turn(monster, hero)
        label = "CRITICAL! " if crit else ""
        print(f"Turn {turn}: {label}{monster.name} deals {dmg} → {hero.name} HP={hero.hp}")

    if not hero.is_alive:
        print(f"\n{hero.name} has fallen.")
    elif not monster.is_alive:
        print(f"\n{monster.name} defeated! Hero wins.")
    else:
        print("\n(3 turns done — battle continues...)")
