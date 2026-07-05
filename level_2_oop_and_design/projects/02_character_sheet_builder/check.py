"""check.py — Project 02: Character Sheet Builder"""

import dataclasses
import json
import sys
from enum import Enum
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PROGRESS_FILE = Path(__file__).parents[3] / "level_2_oop_and_design" / ".progress"

sys.path.insert(0, str(PROJECT_DIR))


def update_progress(project_id: str) -> None:
    progress: dict = {"missions": {}, "projects": {}}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    progress["projects"][project_id] = "complete"
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


def main() -> None:
    # ── 1. Import ─────────────────────────────────────────────────────────────
    try:
        from task import Armor, CharacterSheet, HeroClass, Weapon
    except ImportError as exc:
        print(f"❌ Cannot import from task.py: {exc}")
        raise SystemExit(1)

    # ── 2. HeroClass is an Enum ───────────────────────────────────────────────
    if not issubclass(HeroClass, Enum):
        print("❌ HeroClass must be an Enum subclass")
        raise SystemExit(1)
    for expected in ("WARRIOR", "MAGE", "RANGER"):
        if not hasattr(HeroClass, expected):
            print(f"❌ HeroClass must have member {expected}")
            raise SystemExit(1)
    print("✓ HeroClass is an Enum with WARRIOR, MAGE, RANGER")

    # ── 3. Weapon and Armor are dataclasses ───────────────────────────────────
    if not dataclasses.is_dataclass(Weapon):
        print("❌ Weapon must be a @dataclass")
        raise SystemExit(1)
    if not dataclasses.is_dataclass(Armor):
        print("❌ Armor must be a @dataclass")
        raise SystemExit(1)
    sword = Weapon(name="Iron Sword", damage=12, weight=3.5)
    vest = Armor(name="Leather Vest", defense=6, weight=6.0)
    print("✓ Weapon and Armor are dataclasses")

    # ── 4. Scaffold guard ─────────────────────────────────────────────────────
    sheet = CharacterSheet(name="Ada", hero_class=HeroClass.WARRIOR, hp=120,
                           weapon=sword, armor=vest)
    try:
        _ = sheet.total_weight
    except NotImplementedError:
        print("❌ task.py is not implemented yet — replace NotImplementedError with real code")
        raise SystemExit(1)

    # ── 5. total_weight ───────────────────────────────────────────────────────
    try:
        expected_weight = 3.5 + 6.0
        assert abs(sheet.total_weight - expected_weight) < 0.001, (
            f"total_weight should be {expected_weight}, got {sheet.total_weight}"
        )
        # no weapon
        sheet_no_weapon = CharacterSheet(name="Rex", hero_class=HeroClass.RANGER,
                                         hp=100, weapon=None, armor=vest)
        assert abs(sheet_no_weapon.total_weight - 6.0) < 0.001, (
            f"total_weight with no weapon should be 6.0, got {sheet_no_weapon.total_weight}"
        )
        # no equipment
        bare = CharacterSheet(name="Zara", hero_class=HeroClass.MAGE, hp=80)
        assert bare.total_weight == 0.0, (
            f"total_weight with no equipment should be 0.0, got {bare.total_weight}"
        )
        print("✓ total_weight: with gear, partial, and empty all correct")
    except AssertionError as exc:
        print(f"❌ {exc}")
        raise SystemExit(1)

    # ── 6. power_score ────────────────────────────────────────────────────────
    try:
        # damage=12, defense=6, total_weight=9.5 → penalty=int(9.5//5)=1 → score=12+6-1=17
        expected_power = 12 + 6 - int(9.5 // 5)
        assert sheet.power_score == expected_power, (
            f"power_score should be {expected_power}, got {sheet.power_score}"
        )
        # bare sheet: 0+0-0=0, minimum 0
        assert bare.power_score >= 0, "power_score must be ≥ 0"
        print(f"✓ power_score correct (Ada: {sheet.power_score})")
    except AssertionError as exc:
        print(f"❌ {exc}")
        raise SystemExit(1)

    # ── 7. is_encumbered ──────────────────────────────────────────────────────
    try:
        assert not sheet.is_encumbered, (
            f"Ada (9.5 kg) should NOT be encumbered, got {sheet.is_encumbered}"
        )
        heavy_armor = Armor("Dragon Plate", defense=20, weight=18.0)
        heavy = CharacterSheet(name="Tank", hero_class=HeroClass.WARRIOR,
                               hp=200, weapon=sword, armor=heavy_armor)
        assert heavy.is_encumbered, (
            f"Tank ({heavy.total_weight} kg) SHOULD be encumbered"
        )
        print("✓ is_encumbered correct")
    except AssertionError as exc:
        print(f"❌ {exc}")
        raise SystemExit(1)

    # ── 8. summary ────────────────────────────────────────────────────────────
    try:
        result = sheet.summary()
        assert isinstance(result, str), "summary() must return a str"
        assert len(result.strip()) > 0, "summary() returned empty string"
        assert "Ada" in result, "summary() must include the hero's name"
        assert "WARRIOR" in result or "warrior" in result, (
            "summary() must include the hero class"
        )
        print(f"✓ summary() returns: {result!r}")
    except AssertionError as exc:
        print(f"❌ {exc}")
        raise SystemExit(1)
    except NotImplementedError:
        print("❌ summary() not implemented")
        raise SystemExit(1)

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("02_character_sheet_builder")
    print()
    print("✅ Project 02 complete: Character Sheet Builder works!")
    print()
    print("   Enum + @dataclass + @property + type hints — all in one clean design.")
    print("   This is what modern Python data modeling looks like.")


if __name__ == "__main__":
    main()
