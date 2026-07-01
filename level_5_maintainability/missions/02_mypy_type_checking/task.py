# task.py — Mission 02: mypy_type_checking
#
# A complete RPG using Level 4 concepts (Typer, logging, Rich, Pydantic, reports).
# The code WORKS and is ruff-clean — but type annotations are missing everywhere.
# Level 5 Mission 02 fixes this.
#
# Smell 2 (M02): No type annotations on functions or methods
# Smell 3 (M03): No pyright config — type errors lurk but go undetected
# Smell 4 (M04/M05/M06): No tests — a one-line change can silently break everything
# Smell 5 (M07): Bare except swallows errors; no custom exception hierarchy
# Smell 6 (M08/M09): No pre-commit hooks; no CI — bad code reaches main unchecked
#

import copy
import json
import logging
import random
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path

import typer
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="rpg",
    help="RPG Dungeon — a terminal role-playing game.",
    no_args_is_help=True,
)
console = Console()
logger = logging.getLogger(__name__)

_ROOT = Path(__file__).parent
DATA_DIR = _ROOT / "data"
SAVES_DIR = _ROOT / "saves"
SAVE_FILE = SAVES_DIR / "save_game.json"
LOG_FILE = SAVES_DIR / "app.log"
REPORTS_DIR = _ROOT / "reports"
CURRENT_SCHEMA_VERSION = 1


class HeroClass(StrEnum):
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

    @property
    def is_alive(self):  # TODO: add -> bool
        return self.hp > 0

    def take_damage(self, amount):  # TODO: add type annotations
        self.hp = max(0, self.hp - amount)

    def use_potion(self):  # TODO: add -> bool
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
    def is_alive(self):  # TODO: add -> bool
        return self.hp > 0

    def take_damage(self, amount):  # TODO: add type annotation
        self.hp = max(0, self.hp - amount)


class MonsterConfig(BaseModel):
    name: str
    hp: int = Field(gt=0)
    atk: int = Field(ge=1)
    def_: int = Field(ge=0, alias="def")
    gold: int = Field(ge=0)
    model_config = {"populate_by_name": True}

    def to_domain(self) -> Monster:
        return Monster(
            name=self.name,
            hp=self.hp,
            atk=self.atk,
            def_=self.def_,
            gold=self.gold,
        )


class SaveGameModel(BaseModel):
    schema_version: int = Field(default=CURRENT_SCHEMA_VERSION, ge=1)
    name: str
    hero_class: str
    hp: int = Field(ge=0)
    max_hp: int = Field(gt=0)
    atk: int = Field(ge=1)
    def_: int = Field(ge=0)
    potions: int = Field(ge=0)
    gold: int = Field(ge=0)
    wins: int = Field(ge=0)
    losses: int = Field(ge=0)

    def to_hero(self) -> Hero:
        return Hero(
            name=self.name,
            hero_class=HeroClass(self.hero_class),
            hp=self.hp,
            max_hp=self.max_hp,
            atk=self.atk,
            def_=self.def_,
            potions=self.potions,
            gold=self.gold,
            wins=self.wins,
            losses=self.losses,
        )

    @classmethod
    def from_hero(cls, hero: Hero) -> "SaveGameModel":
        return cls(
            name=hero.name,
            hero_class=hero.hero_class.value,
            hp=hero.hp,
            max_hp=hero.max_hp,
            atk=hero.atk,
            def_=hero.def_,
            potions=hero.potions,
            gold=hero.gold,
            wins=hero.wins,
            losses=hero.losses,
        )


class SessionSummary(BaseModel):
    started_at: datetime
    hero_name: str
    hero_class: str
    battles: int = Field(ge=0)
    wins: int = Field(ge=0)
    losses: int = Field(ge=0)
    gold_earned: int = Field(ge=0)
    final_hp: int = Field(ge=0)
    max_hp: int = Field(gt=0)

    def to_markdown(self) -> str:
        win_rate = self.wins / self.battles if self.battles > 0 else 0.0
        lines = [
            "# Session Report",
            "",
            f"**Hero:** {self.hero_name} ({self.hero_class})",
            f"**Date:** {self.started_at.strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Combat Summary",
            "",
            "| Stat | Value |",
            "|------|-------|",
            f"| Battles | {self.battles} |",
            f"| Wins | {self.wins} |",
            f"| Win Rate | {win_rate:.0%} |",
            f"| Gold Earned | {self.gold_earned} |",
            f"| Final HP | {self.final_hp}/{self.max_hp} |",
        ]
        return "\n".join(lines) + "\n"


def setup_logging() -> None:
    SAVES_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE)],
    )


def load_monsters():  # TODO: add -> list[Monster]
    try:
        with open(DATA_DIR / "monsters.json") as f:
            raw = json.load(f)
        monsters = []
        for entry in raw["monsters"]:
            try:
                monsters.append(MonsterConfig.model_validate(entry).to_domain())
            except Exception:
                pass
        return monsters
    except Exception:
        return []


def load_hero_classes():  # TODO: add -> dict[str, dict[str, int | str]]
    try:
        with open(DATA_DIR / "hero_classes.json") as f:
            return json.load(f)
    except Exception:
        return {}


def save_hero(hero):  # TODO: add hero: Hero, -> None
    SAVES_DIR.mkdir(parents=True, exist_ok=True)
    SAVE_FILE.write_text(SaveGameModel.from_hero(hero).model_dump_json(indent=2))
    logger.info("Saved hero: %s", hero.name)


def load_hero():  # TODO: add -> Hero | None
    if not SAVE_FILE.exists():
        return None
    try:
        model = SaveGameModel.model_validate_json(SAVE_FILE.read_text())
        if model.schema_version != CURRENT_SCHEMA_VERSION:
            return None
        return model.to_hero()
    except Exception:
        return None


def compute_damage(atk, def_, roll):  # TODO: add int annotations -> int
    return max(1, atk + roll - def_)


def make_hero(name, hero_class):  # TODO: add str, HeroClass -> Hero
    classes = load_hero_classes()
    d = classes.get(hero_class.value, {"hp": 100, "atk": 10, "def": 3})
    return Hero(
        name=name,
        hero_class=hero_class,
        hp=d["hp"],
        max_hp=d["hp"],
        atk=d["atk"],
        def_=d["def"],
    )


def simulate_one(hero, monster):  # TODO: add Hero, Monster -> bool
    while hero.is_alive and monster.is_alive:
        dmg = compute_damage(hero.atk, monster.def_, random.randint(1, 6))
        monster.take_damage(dmg)
        if not monster.is_alive:
            hero.gold += monster.gold
            hero.wins += 1
            return True
        hero.take_damage(
            compute_damage(monster.atk, hero.def_, random.randint(1, 6))
        )
        if not hero.is_alive:
            hero.losses += 1
            return False
    return hero.is_alive


def generate_reports(session):  # TODO: add SessionSummary -> tuple[Path, Path]
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = session.started_at.strftime("%Y-%m-%d_%H%M")
    json_path = REPORTS_DIR / f"session_{ts}.json"
    md_path = REPORTS_DIR / f"session_{ts}.md"
    json_path.write_text(session.model_dump_json(indent=2))
    md_path.write_text(session.to_markdown())
    return json_path, md_path


@app.command("new-game")
def new_game(
    name: str = typer.Option("Hero", "--name"),
    hero_class: HeroClass = typer.Option(HeroClass.warrior, "--class"),
) -> None:
    """Create a new hero and save it."""
    setup_logging()
    hero = make_hero(name, hero_class)
    save_hero(hero)
    console.print(f"[green]New hero created:[/green] {name} the {hero_class.value}")
    logger.info("New hero: %s (%s)", name, hero_class.value)


@app.command()
def simulate(battles: int = typer.Option(5, "--battles")) -> None:
    """Auto-simulate N battles without interactive prompts."""
    setup_logging()
    hero = load_hero()
    if hero is None:
        console.print("[red]No save found. Run new-game first.[/red]")
        raise typer.Exit(1)
    monsters = load_monsters()
    if not monsters:
        console.print("[red]No monsters found in data/.[/red]")
        raise typer.Exit(1)
    started_at = datetime.now()
    gold_start = hero.gold
    battles_start = hero.wins + hero.losses
    for _ in range(battles):
        if not hero.is_alive:
            break
        simulate_one(hero, copy.deepcopy(random.choice(monsters)))
    session = SessionSummary(
        started_at=started_at,
        hero_name=hero.name,
        hero_class=hero.hero_class.value,
        battles=hero.wins + hero.losses - battles_start,
        wins=hero.wins,
        losses=hero.losses,
        gold_earned=hero.gold - gold_start,
        final_hp=hero.hp,
        max_hp=hero.max_hp,
    )
    save_hero(hero)
    json_path, md_path = generate_reports(session)
    table = Table(title="Simulation Complete")
    table.add_column("Stat")
    table.add_column("Value")
    table.add_row("Battles", str(battles))
    table.add_row("Wins", str(hero.wins))
    table.add_row("Gold", str(hero.gold))
    table.add_row("HP", f"{hero.hp}/{hero.max_hp}")
    console.print(table)
    console.print(f"[blue]Reports:[/blue] {json_path.name}, {md_path.name}")


@app.command()
def status() -> None:
    """Show current hero status."""
    setup_logging()
    hero = load_hero()
    if hero is None:
        console.print("No save found. Run new-game first.")
        return
    table = Table(title=f"{hero.name} ({hero.hero_class.value})")
    table.add_column("Stat")
    table.add_column("Value")
    for stat, val in [
        ("HP", f"{hero.hp}/{hero.max_hp}"),
        ("ATK", str(hero.atk)),
        ("DEF", str(hero.def_)),
        ("Gold", str(hero.gold)),
        ("Potions", str(hero.potions)),
        ("W/L", f"{hero.wins}/{hero.losses}"),
    ]:
        table.add_row(stat, val)
    console.print(table)


@app.command()
def report() -> None:
    """Show the most recent session report."""
    setup_logging()
    reports = sorted(REPORTS_DIR.glob("*.md")) if REPORTS_DIR.exists() else []
    if not reports:
        console.print("No reports found. Run simulate first.")
        return
    console.print(reports[-1].read_text())


if __name__ == "__main__":
    app()
