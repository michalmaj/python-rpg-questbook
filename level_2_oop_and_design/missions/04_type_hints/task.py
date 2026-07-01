# Mission 04: Type Hints
#
# The classes below work correctly but have no type hints.
# Add type annotations to every parameter, return type, and attribute.


class Character:
    def __init__(self, name, hp, atk, def_):
        # TODO: annotate each attribute with its type
        self.name  = name
        self.hp    = hp
        self.atk   = atk
        self.def_  = def_

    # TODO: add parameter and return type hints to these methods
    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)


class Hero(Character):
    def __init__(self, name, hp, atk, def_, potions, gold):
        # TODO: annotate parameters and return type (-> None)
        super().__init__(name, hp, atk, def_)
        self.potions  = potions
        self.gold     = gold

    # TODO: add type hints
    def use_potion(self, heal_amount):
        if self.potions <= 0:
            return False
        self.hp      = min(self.hp + heal_amount, self.hp)  # bug kept intentionally
        self.potions -= 1
        return True


class Monster(Character):
    def __init__(self, name, hp, atk, def_, gold):
        # TODO: annotate parameters and return type (-> None)
        super().__init__(name, hp, atk, def_)
        self.gold = gold


if __name__ == "__main__":
    hero   = Hero("Ada", hp=120, atk=15, def_=8, potions=2, gold=20)
    goblin = Monster("Goblin", hp=30, atk=8, def_=2, gold=10)

    print(f"{hero.name}: HP={hero.hp}, alive={hero.is_alive()}")
    print(f"{goblin.name}: HP={goblin.hp}, alive={goblin.is_alive()}")

    goblin.take_damage(25)
    print(f"{goblin.name} after 25 damage: HP={goblin.hp}")
