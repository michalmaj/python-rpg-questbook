# Pydantic boundary models — save file schema and session report.
# Domain never imports from here.

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field

from rpg.domain import Hero, HeroClass  # noqa: F401

CURRENT_SCHEMA_VERSION = 1


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
            hp=self.hp, max_hp=self.max_hp,
            atk=self.atk, def_=self.def_,
            potions=self.potions, gold=self.gold,
            wins=self.wins, losses=self.losses,
        )

    @classmethod
    def from_hero(cls, hero: Hero) -> "SaveGameModel":
        return cls(
            name=hero.name, hero_class=hero.hero_class.value,
            hp=hero.hp, max_hp=hero.max_hp,
            atk=hero.atk, def_=hero.def_,
            potions=hero.potions, gold=hero.gold,
            wins=hero.wins, losses=hero.losses,
        )


class SessionSummary(BaseModel):
    """One complete play/simulate session."""

    started_at: datetime
    hero_name: str
    hero_class: str
    battles: int = Field(ge=0)
    wins: int = Field(ge=0)
    losses: int = Field(ge=0)
    gold_earned: int = Field(ge=0)
    final_hp: int = Field(ge=0)
    max_hp: int = Field(gt=0)

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

    def to_markdown(self) -> str:
        # TODO: return a Markdown string with hero name, class, date,
        # battles, wins, losses, gold, final HP.
        raise NotImplementedError


def save_hero(hero: Hero, path: Path) -> None:
    """Persist a hero to JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(SaveGameModel.from_hero(hero).model_dump_json(indent=2))


def load_hero(path: Path) -> Hero | None:
    """Load hero from JSON; return None if file missing or invalid."""
    from pydantic import ValidationError
    if not path.exists():
        return None
    try:
        model = SaveGameModel.model_validate_json(path.read_text())
        if model.schema_version != CURRENT_SCHEMA_VERSION:
            return None
        return model.to_hero()
    except (ValidationError, ValueError):
        return None
