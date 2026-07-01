# Mission 06: Properties
#
# Add @property methods to Character for computed values.


class Character:
    def __init__(self, name: str, hp: int, max_hp: int, atk: int, def_: int) -> None:
        self.name    = name
        self.hp      = hp
        self.max_hp  = max_hp
        self.atk     = atk
        self.def_    = def_

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)

    # TODO 1: Add a property 'is_alive' that returns True if hp > 0.

    # TODO 2: Add a property 'hp_percent' that returns hp as a percentage
    #         of max_hp (a float between 0.0 and 100.0).
    #         Example: hp=85, max_hp=120 → 70.83...

    # TODO 3: Add a property 'status' that returns:
    #           "healthy"  if hp_percent >= 50
    #           "wounded"  if hp_percent >= 20
    #           "critical" otherwise


if __name__ == "__main__":
    hero = Character("Ada", hp=120, max_hp=120, atk=15, def_=8)
    print(f"HP: {hero.hp}/{hero.max_hp}")
    print(f"Alive: {hero.is_alive}")
    print(f"Status: {hero.status}")

    hero.take_damage(60)
    print("\nAfter 60 damage:")
    print(f"HP: {hero.hp}/{hero.max_hp}")
    print(f"Percent: {hero.hp_percent:.1f}%")
    print(f"Status: {hero.status}")

    hero.take_damage(50)
    print("\nAfter 50 more damage:")
    print(f"HP: {hero.hp}/{hero.max_hp}")
    print(f"Status: {hero.status}")
    print(f"Alive: {hero.is_alive}")
