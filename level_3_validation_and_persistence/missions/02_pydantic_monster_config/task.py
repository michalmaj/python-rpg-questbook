"""
Mission 02: Pydantic Monster Config

In Mission 01 you wrote validate_monster() by hand — checking types,
missing fields, and constraints one by one.

Pydantic does all of that with one model definition.

Your task: define MonsterConfig and WeaponConfig as Pydantic models.
"""

import json
from pathlib import Path

# from pydantic import BaseModel, Field, ValidationError  # uncomment when ready

MONSTERS_FILE = Path(__file__).parent / "monsters.json"


# ---------------------------------------------------------------------------
# TODO: Define MonsterConfig
#
# It must validate:
#   name  : str
#   hp    : int  — must be > 0         hint: Field(gt=0)
#   atk   : int  — must be >= 1        hint: Field(ge=1)
#   def_  : int  — must be >= 0        hint: Field(ge=0)
#   gold  : int  — must be >= 0        hint: Field(ge=0)
#
# The JSON key is "def" but Python can't use "def" as a variable name.
# Use Field(alias="def") to map "def" → def_:
#
#   from pydantic import Field
#   def_: int = Field(ge=0, alias="def")
#
# Also add model_config = ConfigDict(populate_by_name=True) so the model
# works whether you pass alias or field name.
# ---------------------------------------------------------------------------

# class MonsterConfig(BaseModel):
#     ...


# ---------------------------------------------------------------------------
# TODO: Define WeaponConfig
#
# It must validate:
#   name      : str
#   atk_bonus : int  — must be >= 0    hint: Field(ge=0)
#   price     : int  — must be >= 0    hint: Field(ge=0)
# ---------------------------------------------------------------------------

# class WeaponConfig(BaseModel):
#     ...


# ---------------------------------------------------------------------------
# runner
# ---------------------------------------------------------------------------


def main() -> None:
    print("=== Loading monsters.json with MonsterConfig ===\n")
    with open(MONSTERS_FILE) as f:
        raw = json.load(f)

    for entry in raw["monsters"]:
        try:
            # monster = MonsterConfig.model_validate(entry)
            # print(f"  ✅ {monster.name}: hp={monster.hp}, atk={monster.atk}")
            pass
        except Exception as e:
            print(f"  ❌ Validation error: {e}")

    print("\n=== Testing with bad data ===\n")
    bad_examples = [
        {"name": "Ghost",  "hp": -50, "atk": 8, "def": 2, "gold": 15},
        {"name": "Slime",  "hp": "lots", "atk": 5, "def": 1, "gold": 5},
        {"name": "Bandit", "atk": 10, "def": 3, "gold": 20},
    ]
    for entry in bad_examples:
        try:
            # config = MonsterConfig.model_validate(entry)
            # print(f"  ✅ {config.name}")
            pass
        except Exception as e:
            print(f"  ❌ {entry.get('name', '?')}: {e}")


if __name__ == "__main__":
    main()
