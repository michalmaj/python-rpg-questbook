"""
Mission 01: argparse Baseline

The starter RPG always uses input() — it cannot be run without a human
pressing keys. A CLI interface lets you pass arguments upfront:

    python game.py new-game --name Ada --class warrior
    python game.py simulate --battles 10
    python game.py status

Your task: implement make_parser(), then the three command handlers.
The game logic (load_monsters, choose_hero, run_combat, ...) is already
imported from game_logic — you only write the interface layer.
"""

import argparse
import random
import sys

from pathlib import Path
from dataclasses import dataclass
from enum import Enum

# ----- minimal domain (self-contained for the mission) -----------------------

DATA_DIR = Path(__file__).parent / "data"
SAVES_DIR = Path(__file__).parent / "saves"
SAVE_FILE = SAVES_DIR / "save_game.json"


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


HERO_TEMPLATES: dict[str, dict] = {
    "warrior": {"hp": 120, "atk": 12, "def_": 4},
    "mage":    {"hp": 80,  "atk": 18, "def_": 2},
    "rogue":   {"hp": 100, "atk": 14, "def_": 3},
}

MONSTERS: list[dict] = [
    {"name": "Goblin",  "hp": 30,  "atk": 8,  "def_": 2,  "gold": 10},
    {"name": "Orc",     "hp": 50,  "atk": 12, "def_": 4,  "gold": 20},
    {"name": "Troll",   "hp": 80,  "atk": 16, "def_": 6,  "gold": 40},
]


def make_hero(name: str, hero_class: str) -> Hero:
    t = HERO_TEMPLATES[hero_class]
    return Hero(name=name, hero_class=HeroClass(hero_class),
                hp=t["hp"], max_hp=t["hp"], atk=t["atk"], def_=t["def_"])


def simulate_battles(hero: Hero, battles: int) -> None:
    """Run N auto-battles (no input required) and print a summary."""
    wins = 0
    for i in range(battles):
        m = random.choice(MONSTERS)
        mhp = m["hp"]
        hhp = hero.hp
        # simplified auto-combat
        while hhp > 0 and mhp > 0:
            dice = random.randint(1, 6)
            mhp -= max(1, hero.atk + dice - m["def_"])
            if mhp <= 0:
                break
            dice = random.randint(1, 6)
            hhp -= max(1, m["atk"] + dice - hero.def_)
        if hhp > 0:
            wins += 1
            hero.gold += m["gold"]
    print(f"Simulated {battles} battles: {wins} wins, {battles - wins} losses. Gold: {hero.gold}")


def load_save() -> Hero | None:
    """Return saved hero or None if no save exists."""
    import json
    if not SAVE_FILE.exists():
        return None
    try:
        data = json.loads(SAVE_FILE.read_text())
        return Hero(
            name=data["name"],
            hero_class=HeroClass(data["hero_class"]),
            hp=data["hp"], max_hp=data["max_hp"],
            atk=data["atk"], def_=data["def_"],
            potions=data.get("potions", 3),
            gold=data.get("gold", 0),
            wins=data.get("wins", 0),
            losses=data.get("losses", 0),
        )
    except Exception:
        return None


def save_hero(hero: Hero) -> None:
    import json
    SAVES_DIR.mkdir(exist_ok=True)
    SAVE_FILE.write_text(json.dumps({
        "name": hero.name, "hero_class": hero.hero_class.value,
        "hp": hero.hp, "max_hp": hero.max_hp, "atk": hero.atk, "def_": hero.def_,
        "potions": hero.potions, "gold": hero.gold, "wins": hero.wins, "losses": hero.losses,
    }, indent=2))


# ----- your work starts here -------------------------------------------------


def make_parser() -> argparse.ArgumentParser:
    # TODO:
    # 1. Create ArgumentParser with description="RPG Dungeon CLI"
    # 2. Add subparsers with dest="command", metavar="COMMAND"
    # 3. Add subcommand "new-game":
    #    - --name NAME          (default "Hero")
    #    - --class CLASS        (dest="hero_class", choices=["warrior","mage","rogue"], default="warrior")
    # 4. Add subcommand "simulate":
    #    - --battles N          (type=int, default=5, help="number of battles to simulate")
    # 5. Add subcommand "status" (no arguments)
    raise NotImplementedError


def cmd_new_game(args: argparse.Namespace) -> None:
    # TODO:
    # 1. Create a hero from args.name and args.hero_class using make_hero()
    # 2. Save the hero using save_hero()
    # 3. Print a confirmation: "New game started: <name> the <class>"
    raise NotImplementedError


def cmd_simulate(args: argparse.Namespace) -> None:
    # TODO:
    # 1. Load saved hero with load_save(); if None, print error and sys.exit(1)
    # 2. Call simulate_battles(hero, args.battles)
    # 3. Save the hero with save_hero()
    raise NotImplementedError


def cmd_status() -> None:
    # TODO:
    # 1. Load saved hero with load_save()
    # 2. If None: print "No save found." and return
    # 3. Print: hero name, class, hp/max_hp, gold, wins/losses
    raise NotImplementedError


def main() -> None:
    try:
        parser = make_parser()
    except NotImplementedError:
        print("TODO: implement make_parser() first.")
        return

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "new-game":
            cmd_new_game(args)
        elif args.command == "simulate":
            cmd_simulate(args)
        elif args.command == "status":
            cmd_status()
    except NotImplementedError:
        print(f"TODO: implement cmd_{args.command.replace('-', '_')}() first.")
        sys.exit(1)


if __name__ == "__main__":
    main()
