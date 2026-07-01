"""check.py — Project 01: Refactored RPG"""

import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]
PROJECT_DIR = Path(__file__).parent
PROGRESS_FILE = REPO_ROOT / "level_2_oop_and_design" / ".progress"

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
    errors: list[str] = []

    # ── 1. File structure ─────────────────────────────────────────────────────
    required_files = [
        PROJECT_DIR / "rpg" / "__init__.py",
        PROJECT_DIR / "rpg" / "hero.py",
        PROJECT_DIR / "rpg" / "monster.py",
        PROJECT_DIR / "rpg" / "combat.py",
        PROJECT_DIR / "rpg" / "game.py",
        PROJECT_DIR / "tests" / "test_combat.py",
    ]
    for path in required_files:
        if not path.exists():
            errors.append(f"Missing file: {path.relative_to(PROJECT_DIR)}")

    if errors:
        print("❌ Missing files:")
        for e in errors:
            print(f"   {e}")
        raise SystemExit(1)

    # ── 2. Imports ────────────────────────────────────────────────────────────
    try:
        from rpg.hero    import Hero, HeroClass
        from rpg.monster import Monster, MonsterTemplate
        from rpg.combat  import compute_damage
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all classes and functions are defined in the rpg/ package.")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ Error loading rpg package: {e}")
        raise SystemExit(1)

    # ── 3. Classes and Enum ───────────────────────────────────────────────────
    try:
        from enum import Enum
        import dataclasses

        assert issubclass(HeroClass, Enum), "HeroClass must be an Enum subclass"
        assert dataclasses.is_dataclass(MonsterTemplate), "MonsterTemplate must be a @dataclass"

        h = Hero("Ada", HeroClass.WARRIOR, hp=120, max_hp=120, atk=15, def_=8, potions=2, gold=20)
        assert h.is_alive, "Hero.is_alive property should work"
        h.take_damage(120)
        assert not h.is_alive, "Hero.is_alive should be False at 0 hp"

        m_tmpl = MonsterTemplate("Goblin", hp=30, atk=8, def_=2, gold=10)
        m = Monster(m_tmpl)
        assert m.is_alive
        m.take_damage(30)
        assert not m.is_alive

    except AssertionError as e:
        print(f"❌ {e}")
        raise SystemExit(1)

    # ── 4. compute_damage is pure (no prints) ─────────────────────────────────
    try:
        buf = io.StringIO()
        with redirect_stdout(buf):
            result = compute_damage(15, 5, 4)
        assert buf.getvalue() == "", "compute_damage should not print anything"
        assert result == 14, f"compute_damage(15, 5, 4) should be 14, got {result}"
        assert compute_damage(1, 100, 1) == 1, "compute_damage minimum should be 1"
    except AssertionError as e:
        print(f"❌ {e}")
        raise SystemExit(1)

    # ── 5. Tests pass ─────────────────────────────────────────────────────────
    result = __import__("subprocess").run(
        [sys.executable, "-m", "pytest",
         str(PROJECT_DIR / "tests" / "test_combat.py"), "-v", "--tb=short"],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_DIR),
    )
    print(result.stdout)
    if result.returncode != 0:
        print("❌ Tests are failing. Fix tests/test_combat.py and try again.")
        raise SystemExit(1)

    test_source = (PROJECT_DIR / "tests" / "test_combat.py").read_text()
    assert_count = test_source.count("assert ")
    if assert_count < 5:
        print(f"❌ Found {assert_count} assert(s). Write at least 5 test assertions.")
        raise SystemExit(1)

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("01_refactored_rpg")
    print("✅ Project 01 complete: Refactored RPG passes all checks!")
    print()
    print("   The game plays the same. The code is completely different.")
    print("   That is what professional refactoring looks like.")


if __name__ == "__main__":
    main()
