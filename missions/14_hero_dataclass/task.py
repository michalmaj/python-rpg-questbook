from dataclasses import dataclass


@dataclass
class Hero:
    name: str
    hero_class: str
    hp: int
    max_hp: int
    level: int
    gold: int


# TODO: Create a Hero named "Ada", class "Warrior", hp=100, max_hp=100, level=1, gold=50
hero = Hero(
    name=None,
    hero_class=None,
    hp=None,
    max_hp=None,
    level=None,
    gold=None,
)

# TODO: Take 30 damage — subtract 30 from hero.hp
# hero.hp -= ...

# TODO: Earn 25 gold — add 25 to hero.gold
# hero.gold += ...

print(f"Name:  {hero.name}")
print(f"Class: {hero.hero_class}")
print(f"HP:    {hero.hp}/{hero.max_hp}")
print(f"Gold:  {hero.gold}")
