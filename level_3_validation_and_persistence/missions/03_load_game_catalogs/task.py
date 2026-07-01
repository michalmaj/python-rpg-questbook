"""
Mission 03: Load Game Catalogs

Pydantic validates the data at the boundary.
But the game uses domain dataclasses (Monster, Weapon), not Pydantic models.

Your task: complete the pipeline

    JSON file  →  Pydantic config model  →  domain dataclass

The pattern keeps the domain clean: game logic never touches Pydantic,
and Pydantic models never leak into combat or save logic.
"""

import json  # noqa: F401
from dataclasses import dataclass
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field

DATA_DIR = Path(__file__).parent


# ----- domain dataclasses (unchanged from Level 2) ---------------------------


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


@dataclass
class Weapon:
    name: str
    atk_bonus: int
    price: int


# ----- Pydantic config models (boundary layer) --------------------------------


class MonsterConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    hp:   int = Field(gt=0)
    atk:  int = Field(ge=1)
    def_: int = Field(ge=0, alias="def")
    gold: int = Field(ge=0)

    def to_domain(self) -> Monster:
        """Convert validated config → domain Monster."""
        # TODO: return Monster(name=self.name, hp=self.hp, ...)
        raise NotImplementedError


class WeaponConfig(BaseModel):
    name:      str
    atk_bonus: int = Field(ge=0)
    price:     int = Field(ge=0)

    def to_domain(self) -> Weapon:
        """Convert validated config → domain Weapon."""
        # TODO: return Weapon(...)
        raise NotImplementedError


# ----- catalog loaders --------------------------------------------------------


def load_monsters(path: Path = DATA_DIR / "monsters.json") -> list[Monster]:
    """
    Load and validate monsters from a JSON file.
    Return a list of domain Monster objects.
    Skip (and print a warning for) any entry that fails validation.
    """
    # TODO:
    # 1. Read and parse the JSON file
    # 2. For each entry in raw["monsters"]:
    #      - call MonsterConfig.model_validate(entry)
    #      - if ValidationError: print a warning and skip
    #      - else: call config.to_domain() and add to result list
    # 3. Return the list
    raise NotImplementedError


def load_weapons(path: Path = DATA_DIR / "weapons.json") -> list[Weapon]:
    """
    Load and validate weapons from a JSON file.
    Return a list of domain Weapon objects.
    Skip (and print a warning for) any entry that fails validation.
    """
    # TODO: same pattern as load_monsters
    raise NotImplementedError


# ----- runner -----------------------------------------------------------------


def main() -> None:
    try:
        monsters = load_monsters()
    except NotImplementedError:
        print("TODO: implement MonsterConfig.to_domain() and load_monsters() first.")
        return
    print(f"Loaded {len(monsters)} monsters:")
    for m in monsters:
        print(f"  {m.name}: hp={m.hp}, atk={m.atk}, def={m.def_}")

    try:
        weapons = load_weapons()
    except NotImplementedError:
        print("TODO: implement WeaponConfig.to_domain() and load_weapons() first.")
        return
    print(f"\nLoaded {len(weapons)} weapons:")
    for w in weapons:
        print(f"  {w.name}: +{w.atk_bonus} atk, {w.price} gold")


if __name__ == "__main__":
    main()
