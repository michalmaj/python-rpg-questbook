"""
Mission 02: Typer CLI

Mission 01 built the same three commands using argparse — lots of plumbing.
Now rewrite them using Typer: type hints become the CLI contract.

    python task.py new-game --name Ada --class warrior
    python task.py simulate --battles 10
    python task.py status

Your job: create `app = typer.Typer()` and decorate three functions.
"""

import json
import random
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Annotated  # noqa: F401

import typer

# ----- domain (same as M01) --------------------------------------------------

SAVES_DIR = Path(__file__).parent / "saves"
SAVE_FILE = SAVES_DIR / "save_game.json"


class HeroClass(str, Enum):
    warrior = "warrior"
    mage = "mage"
    rogue = "rogue"


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


def _make_hero(name: str, hero_class: HeroClass) -> Hero:
    t = HERO_TEMPLATES[hero_class.value]
    return Hero(name=name, hero_class=hero_class,
                hp=t["hp"], max_hp=t["hp"], atk=t["atk"], def_=t["def_"])


def _simulate_battles(hero: Hero, battles: int) -> None:
    wins = 0
    for _ in range(battles):
        m = random.choice(MONSTERS)
        mhp, hhp = m["hp"], hero.hp
        while hhp > 0 and mhp > 0:
            mhp -= max(1, hero.atk + random.randint(1, 6) - m["def_"])
            if mhp <= 0:
                break
            hhp -= max(1, m["atk"] + random.randint(1, 6) - hero.def_)
        if hhp > 0:
            wins += 1
            hero.gold += m["gold"]
    typer.echo(f"Simulated {battles} battles: {wins} wins, {battles - wins} losses. Gold: {hero.gold}")


def _load_save() -> Hero | None:
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


def _save_hero(hero: Hero) -> None:
    SAVES_DIR.mkdir(exist_ok=True)
    SAVE_FILE.write_text(json.dumps({
        "name": hero.name, "hero_class": hero.hero_class.value,
        "hp": hero.hp, "max_hp": hero.max_hp, "atk": hero.atk, "def_": hero.def_,
        "potions": hero.potions, "gold": hero.gold, "wins": hero.wins, "losses": hero.losses,
    }, indent=2))


# ----- your work starts here -------------------------------------------------

# TODO: create the Typer app
# app = typer.Typer()


# TODO: decorate this function so it becomes the "new-game" subcommand.
# Parameters:
#   name:       Annotated[str, typer.Option("--name", help="Hero name")] = "Hero"
#   hero_class: Annotated[HeroClass, typer.Option("--class", "--hero-class",
#               help="Hero class")] = HeroClass.warrior
def new_game(
    name: str = "Hero",
    hero_class: HeroClass = HeroClass.warrior,
) -> None:
    # TODO:
    # 1. Create hero with _make_hero(name, hero_class)
    # 2. Save with _save_hero(hero)
    # 3. typer.echo(f"New game started: {name} the {hero_class.value}")
    raise NotImplementedError


# TODO: decorate this function so it becomes the "simulate" subcommand.
# Parameters:
#   battles: Annotated[int, typer.Option("--battles", help="Number of battles")] = 5
def simulate(battles: int = 5) -> None:
    # TODO:
    # 1. Load save with _load_save(); if None: typer.echo("No save found."); raise typer.Exit(1)
    # 2. _simulate_battles(hero, battles)
    # 3. _save_hero(hero)
    raise NotImplementedError


# TODO: decorate this function so it becomes the "status" subcommand.
def status() -> None:
    # TODO:
    # 1. Load save with _load_save()
    # 2. If None: typer.echo("No save found."); return
    # 3. Print hero name, class, hp/max_hp, gold, wins/losses
    raise NotImplementedError


# TODO: add:  if __name__ == "__main__": app()
