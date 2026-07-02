"""conftest.py — fixtures for M06 (pre-provided; focus is on coverage in test_combat.py)."""
import pytest
from rpg import Hero, HeroClass, Monster


@pytest.fixture
def warrior() -> Hero:
    return Hero(name="Ada", hero_class=HeroClass.warrior, hp=120, max_hp=120, atk=12, def_=5)


@pytest.fixture
def goblin() -> Monster:
    return Monster(name="Goblin", hp=30, atk=8, def_=2, gold=10)


@pytest.fixture
def make_hero():
    def _make(**kwargs: object) -> Hero:
        defaults: dict[str, object] = dict(
            name="TestHero", hero_class=HeroClass.warrior,
            hp=120, max_hp=120, atk=12, def_=5,
        )
        return Hero(**{**defaults, **kwargs})  # type: ignore[arg-type]
    return _make
