"""
Mission 01: External Data Is Untrusted

The game loads monster data from a JSON file.
But what if the file has bad data? Run this file to find out.

Then write validate_monster() to detect the problems.
"""

import json
from pathlib import Path

BROKEN_FILE = Path(__file__).parent / "broken_monsters.json"


# --- Part 1: naive loading (already written — just run it and observe) --------


def naive_load() -> None:
    """Load monsters without any validation and try to use them."""
    with open(BROKEN_FILE) as f:
        data = json.load(f)

    for entry in data["monsters"]:
        name = entry["name"]
        hp = entry["hp"]          # might be missing or a string
        atk = entry["atk"]
        print(f"  {name}: hp={hp}, atk={atk}, damage would be {atk + 3 - 2}")


# --- Part 2: your task --------------------------------------------------------


def validate_monster(raw: dict) -> list[str]:
    """
    Check one monster dict from the JSON file.

    Return a list of error strings describing every problem found.
    Return an empty list if the monster is valid.

    Rules:
    - "name" must be present and must be a str
    - "hp" must be present, must be an int, and must be > 0
    - "atk" must be present and must be an int >= 1
    - "def" must be present and must be an int >= 0
    - "gold" must be present and must be an int >= 0
    """
    errors: list[str] = []

    # TODO: check each field and append an error string if invalid
    # Example: errors.append("hp: missing")
    #          errors.append("hp: must be int, got str")
    #          errors.append("hp: must be > 0, got -50")

    return errors


# --- runner -------------------------------------------------------------------


def main() -> None:
    print("=== Part 1: naive loading ===")
    try:
        naive_load()
    except Exception as e:
        print(f"  Crashed: {e}")

    print("\n=== Part 2: your validate_monster() ===")
    with open(BROKEN_FILE) as f:
        data = json.load(f)

    for entry in data["monsters"]:
        name = entry.get("name", "<no name>")
        errors = validate_monster(entry)
        if errors:
            print(f"  ❌ {name}: {'; '.join(errors)}")
        else:
            print(f"  ✅ {name}: valid")


if __name__ == "__main__":
    main()
