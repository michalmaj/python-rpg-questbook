"""
Mission 05: Repository Pattern

save_game() and load_game() are functions — they know they write to JSON.
If you ever want to switch to SQLite, you must change the game code too.

The repository pattern wraps persistence behind a Protocol (interface).
Game code calls repo.save(hero) and repo.load() — it doesn't know whether
the backend is JSON, SQLite, or an in-memory dict for tests.

Your task: define SaveRepository (Protocol) and implement JsonSaveRepository.
"""

import json  # noqa: F401
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, Field

SAVES_DIR = Path(__file__).parent / "saves"
CURRENT_SCHEMA_VERSION = 1


# ----- domain -----------------------------------------------------------------


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


# ----- Pydantic save model (from Mission 04, fully implemented) ---------------


class SaveGameModel(BaseModel):
    schema_version: int = Field(default=CURRENT_SCHEMA_VERSION, ge=1)
    name:       str
    hero_class: str
    hp:         int = Field(ge=0)
    max_hp:     int = Field(gt=0)
    atk:        int = Field(ge=1)
    def_:       int = Field(ge=0)
    potions:    int = Field(ge=0)
    gold:       int = Field(ge=0)
    wins:       int = Field(ge=0)
    losses:     int = Field(ge=0)

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


# ----- repository Protocol ----------------------------------------------------


class SaveRepository(Protocol):
    """
    Defines the interface for saving and loading a Hero.

    Any class that implements save() and load() with these signatures
    satisfies this Protocol — no inheritance needed.
    """

    def save(self, hero: Hero) -> None:
        """Persist the hero's current state."""
        ...

    def load(self) -> Hero | None:
        """Load and return the last saved hero, or None if no save exists."""
        ...


# ----- JSON implementation ----------------------------------------------------


class JsonSaveRepository:
    """
    Saves and loads a Hero as a JSON file using SaveGameModel for validation.
    """

    def __init__(self, path: Path = SAVES_DIR / "save_game.json") -> None:
        self.path = path

    def save(self, hero: Hero) -> None:
        # TODO:
        # 1. Create a SaveGameModel from the hero
        # 2. Write model.model_dump_json(indent=2) to self.path
        # 3. Create parent dirs if needed
        raise NotImplementedError

    def load(self) -> Hero | None:
        # TODO:
        # 1. Return None if self.path does not exist
        # 2. Parse with SaveGameModel.model_validate_json(...)
        # 3. Check schema_version — raise ValueError if it doesn't match
        # 4. Return model.to_hero()
        raise NotImplementedError


# ----- in-memory implementation (for tests) -----------------------------------


class InMemorySaveRepository:
    """
    Saves the hero in a dict — no files, no disk.
    Useful for tests that should not touch the filesystem.
    """

    def __init__(self) -> None:
        self._data: Hero | None = None

    def save(self, hero: Hero) -> None:
        # TODO: store the hero in self._data
        raise NotImplementedError

    def load(self) -> Hero | None:
        # TODO: return self._data
        raise NotImplementedError


# ----- runner -----------------------------------------------------------------


def run_game_session(repo: SaveRepository) -> None:
    """
    A minimal game session that uses a repository.
    Notice: this function doesn't know whether repo is JSON or in-memory.
    """
    hero = repo.load()
    if hero is None:
        hero = Hero(
            name="Ada",
            hero_class=HeroClass.WARRIOR,
            hp=120,
            max_hp=120,
            atk=12,
            def_=4,
        )
        print(f"  New hero: {hero.name}")
    else:
        print(f"  Loaded: {hero.name}, HP={hero.hp}, gold={hero.gold}")

    hero.gold += 10
    repo.save(hero)
    print(f"  Saved. Gold is now {hero.gold}.")


def main() -> None:
    print("=== JSON backend ===")
    json_repo = JsonSaveRepository(SAVES_DIR / "save_game.json")
    run_game_session(json_repo)

    print("\n=== In-memory backend ===")
    mem_repo = InMemorySaveRepository()
    run_game_session(mem_repo)
    run_game_session(mem_repo)   # second run should load the saved hero


if __name__ == "__main__":
    main()
