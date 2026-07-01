"""
Mission 05: Rich Terminal Output

The starter RPG prints everything as plain strings. HP, status, errors,
and combat results all look the same. This mission replaces user-facing
output with Rich tables and panels.

Key idea: formatting is useful only when it makes information clearer.
Not for decoration — for readability.

Your task:
1. Implement show_hero_stats() using rich.table.Table
2. Implement show_combat_start() using rich.panel.Panel
3. Implement show_combat_result() using Panel with green/red border
4. Implement show_error() using console.print(stderr=True)
"""

import random
import sys
from dataclasses import dataclass
from enum import Enum
from rich.console import Console
from rich.panel import Panel  # noqa: F401
from rich.table import Table  # noqa: F401
from rich.text import Text  # noqa: F401

# ----- one shared console per module -----------------------------------------

console = Console()

# ----- domain ----------------------------------------------------------------


class HeroClass(Enum):
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"


@dataclass
class Hero:
    name: str
    hero_class: HeroClass
    hp: int
    max_hp: int
    atk: int
    def_: int
    potions: int = 3
    gold: int = 0
    wins: int = 0
    losses: int = 0

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)

    def use_potion(self) -> bool:
        if self.potions <= 0:
            return False
        self.hp = min(self.hp + 30, self.max_hp)
        self.potions -= 1
        return True


@dataclass
class Monster:
    name: str
    hp: int
    atk: int
    def_: int
    gold: int

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)


HERO_TEMPLATES: dict[str, dict] = {
    "warrior": {"hp": 120, "atk": 12, "def_": 4, "description": "High HP and defence"},
    "mage":    {"hp": 80,  "atk": 18, "def_": 2, "description": "High attack, low defence"},
    "rogue":   {"hp": 100, "atk": 14, "def_": 3, "description": "Balanced speed attacker"},
}

MONSTERS: list[dict] = [
    {"name": "Goblin",  "hp": 30,  "atk": 8,  "def_": 2,  "gold": 10},
    {"name": "Orc",     "hp": 50,  "atk": 12, "def_": 4,  "gold": 20},
    {"name": "Troll",   "hp": 80,  "atk": 16, "def_": 6,  "gold": 40},
]


# ----- your work: Rich output functions --------------------------------------


def show_hero_stats(hero: Hero) -> None:
    # TODO: create a Table (no title needed, or use hero.name as title)
    # Add two columns: "Stat" and "Value"
    # Add rows for: Name, Class, HP (show "96 / 120"), Gold, Potions, W / L
    # Use colour for HP: green if hp >= max_hp * 0.5, red otherwise
    # Call: console.print(table)
    raise NotImplementedError


def show_combat_start(hero: Hero, monster: Monster) -> None:
    # TODO: create a Panel announcing the battle
    # Body: f"{hero.name} (HP {hero.hp}) vs {monster.name} (HP {monster.hp})"
    # Title: "⚔ Battle"
    # Call: console.print(panel)
    raise NotImplementedError


def show_combat_result(winner: str, gold_gained: int = 0) -> None:
    # TODO: create a Panel for the outcome
    # If winner == "hero":
    #   text = "Victory!" + (f"\n+{gold_gained} gold" if gold_gained > 0 else "")
    #   border_style = "green"
    # Else:
    #   text = "Defeated!"
    #   border_style = "red"
    # Call: console.print(Panel(text, border_style=border_style))
    raise NotImplementedError


def show_error(message: str) -> None:
    # TODO: console.print(message, style="bold red", stderr=True)
    # stderr=True routes the output to stderr (not stdout)
    raise NotImplementedError


# ----- game logic (uses Rich output) -----------------------------------------


def compute_damage(atk: int, def_: int, dice_roll: int) -> int:
    return max(1, atk + dice_roll - def_)


def make_hero(name: str, hero_class: str) -> Hero:
    t = HERO_TEMPLATES[hero_class]
    return Hero(name=name, hero_class=HeroClass(hero_class),
                hp=t["hp"], max_hp=t["hp"], atk=t["atk"], def_=t["def_"])


def run_combat(hero: Hero, monster: Monster) -> bool:
    try:
        show_combat_start(hero, monster)
    except NotImplementedError:
        print(f"\n⚔  {hero.name} vs {monster.name}!")

    turn = 1
    while hero.is_alive and monster.is_alive:
        print(f"\nTurn {turn} | {hero.name} HP: {hero.hp} | {monster.name} HP: {monster.hp}")
        action = input("Action — [a]ttack / [p]otion: ").strip().lower()

        if action == "p":
            if hero.use_potion():
                print(f"  Used potion. HP: {hero.hp}")
            else:
                print("  No potions left!")
            turn += 1
            continue

        dice = random.randint(1, 6)
        dmg = compute_damage(hero.atk, monster.def_, dice)
        monster.take_damage(dmg)
        print(f"  You deal {dmg} damage. Monster HP: {monster.hp}")

        if not monster.is_alive:
            try:
                show_combat_result("hero", monster.gold)
            except NotImplementedError:
                print(f"\n✅ Victory! +{monster.gold} gold.")
            hero.gold += monster.gold
            hero.wins += 1
            return True

        mdice = random.randint(1, 6)
        mdmg = compute_damage(monster.atk, hero.def_, mdice)
        hero.take_damage(mdmg)
        print(f"  {monster.name} deals {mdmg} damage. Your HP: {hero.hp}")

        if not hero.is_alive:
            try:
                show_combat_result("monster")
            except NotImplementedError:
                print("\n💀 You were defeated.")
            hero.losses += 1
            return False

        turn += 1

    return hero.is_alive


def main() -> None:
    console.print("[bold]RPG Dungeon — Rich Edition[/bold]\n")

    name = input("Hero name: ").strip() or "Hero"
    print("\nClasses: 1=warrior  2=mage  3=rogue")
    choice = input("Choose (1-3): ").strip()
    class_map = {"1": "warrior", "2": "mage", "3": "rogue"}
    hero_class = class_map.get(choice, "warrior")
    hero = make_hero(name, hero_class)

    monsters = [Monster(**{k: v for k, v in m.items()}) for m in MONSTERS]

    while True:
        try:
            show_hero_stats(hero)
        except NotImplementedError:
            print(f"\n{hero.name} | HP: {hero.hp}/{hero.max_hp} | Gold: {hero.gold}")

        print("\n  [f] Fight   [q] Quit")
        cmd = input("> ").strip().lower()

        if cmd == "f":
            monster = random.choice(monsters)
            monster = Monster(
                name=monster.name, hp=monster.hp,
                atk=monster.atk, def_=monster.def_, gold=monster.gold,
            )
            run_combat(hero, monster)
        elif cmd == "q":
            print("Goodbye!")
            break
        else:
            try:
                show_error(f"Unknown command: '{cmd}'")
            except NotImplementedError:
                print(f"Unknown command: '{cmd}'", file=sys.stderr)


if __name__ == "__main__":
    main()
