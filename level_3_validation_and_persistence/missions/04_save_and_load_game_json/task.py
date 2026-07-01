"""
Mission 04: Save and Load Game JSON

The starter game saves a raw dict to save_game.json with no schema version.
If you add a new field in the future, old save files silently break.

Your task: define SaveGameModel (Pydantic) and implement save_game / load_game
using it. Add a schema_version field so you can detect and handle outdated saves.
"""

import json  # noqa: F401
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field

SAVES_DIR = Path(__file__).parent / "saves"
SAVE_FILE = SAVES_DIR / "save_game.json"

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


# ----- Pydantic save model ----------------------------------------------------


class SaveGameModel(BaseModel):
    """
    Validated representation of save_game.json.

    schema_version lets you detect old save files. If a save file was created
    with version 1 and you later add new fields for version 2, you can handle
    the mismatch instead of crashing.
    """

    schema_version: int = Field(default=CURRENT_SCHEMA_VERSION, ge=1)

    # TODO: add all Hero fields here
    # name:       str
    # hero_class: str       (store the .value, not the Enum itself)
    # hp:         int = Field(ge=0)
    # max_hp:     int = Field(gt=0)
    # atk:        int = Field(ge=1)
    # def_:       int = Field(ge=0)
    # potions:    int = Field(ge=0)
    # gold:       int = Field(ge=0)
    # wins:       int = Field(ge=0)
    # losses:     int = Field(ge=0)

    def to_hero(self) -> Hero:
        """Convert validated save data → domain Hero."""
        # TODO: return Hero(name=self.name, hero_class=HeroClass(self.hero_class), ...)
        raise NotImplementedError

    @classmethod
    def from_hero(cls, hero: Hero) -> "SaveGameModel":
        """Convert domain Hero → save model."""
        # TODO: return cls(name=hero.name, hero_class=hero.hero_class.value, ...)
        raise NotImplementedError


# ----- save / load functions --------------------------------------------------


def save_game(hero: Hero, path: Path = SAVE_FILE) -> None:
    """Validate hero state and write it to a JSON save file."""
    # TODO:
    # 1. Create a SaveGameModel from the hero using from_hero()
    # 2. Write model.model_dump_json(indent=2) to the path
    # 3. Create parent directories if needed (path.parent.mkdir(...))
    raise NotImplementedError


def load_game(path: Path = SAVE_FILE) -> Hero | None:
    """
    Load and validate a save file.
    Return a Hero if the file exists and is valid.
    Return None if the file does not exist.
    Raise ValueError if the file exists but schema_version != CURRENT_SCHEMA_VERSION.
    """
    # TODO:
    # 1. Return None if path does not exist
    # 2. Parse the file with SaveGameModel.model_validate_json(...)
    #    - catch ValidationError → raise ValueError with a descriptive message
    # 3. Check schema_version — if it doesn't match CURRENT_SCHEMA_VERSION,
    #    raise ValueError("Save file version X is not supported. Expected Y.")
    # 4. Return model.to_hero()
    raise NotImplementedError


# ----- runner -----------------------------------------------------------------


def main() -> None:
    hero = Hero(
        name="Ada",
        hero_class=HeroClass.WARRIOR,
        hp=100,
        max_hp=120,
        atk=12,
        def_=4,
        potions=2,
        gold=55,
        wins=3,
        losses=1,
    )

    try:
        print("Saving hero...")
        save_game(hero)
        print(f"  Saved to {SAVE_FILE}")
        print(f"  Contents:\n{SAVE_FILE.read_text()}")
    except NotImplementedError:
        print("TODO: implement SaveGameModel fields, from_hero(), and save_game() first.")
        return

    try:
        print("\nLoading hero...")
        loaded = load_game()
        if loaded:
            print(f"  Loaded: {loaded.name} ({loaded.hero_class.value}), HP={loaded.hp}, gold={loaded.gold}")
        else:
            print("  No save file found.")
    except NotImplementedError:
        print("TODO: implement to_hero() and load_game() first.")


if __name__ == "__main__":
    main()
