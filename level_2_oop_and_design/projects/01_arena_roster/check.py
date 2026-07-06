"""check.py — Project 01: Arena Roster"""

import io
import json
import sys
from contextlib import redirect_stdout
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
        from task import Character, Hero, Monster, build_roster, print_roster
    except ImportError as exc:
        print(f"❌ Cannot import from task.py: {exc}")
        raise SystemExit(1)

    # ── 2. Scaffold guard ─────────────────────────────────────────────────────
    try:
        Hero("Ada", 120, 120, 15, 8, "warrior", 2)
    except NotImplementedError:
        print("❌ task.py is not implemented yet — replace NotImplementedError with real code")
        raise SystemExit(1)
    except Exception:
        pass

    # ── 3. Inheritance ────────────────────────────────────────────────────────
    try:
        if not issubclass(Hero, Character):
            print("❌ Hero must inherit from Character")
            raise SystemExit(1)
        if not issubclass(Monster, Character):
            print("❌ Monster must inherit from Character")
            raise SystemExit(1)
        print("✓ Hero and Monster both inherit from Character")
    except TypeError as exc:
        print(f"❌ Inheritance check failed: {exc}")
        raise SystemExit(1)

    # ── 4. is_alive and take_damage ───────────────────────────────────────────
    try:
        h = Hero("Ada", 120, 120, 15, 8, "warrior", 2)
        assert h.is_alive(), "Hero.is_alive() should return True at full HP"
        h.take_damage(120)
        assert not h.is_alive(), "Hero.is_alive() should return False at 0 HP"
        h.take_damage(999)
        assert h.hp >= 0, "HP must never go below 0 after take_damage"
        print("✓ is_alive and take_damage work correctly")
    except AssertionError as exc:
        print(f"❌ {exc}")
        raise SystemExit(1)
    except AttributeError as exc:
        print(f"❌ Missing attribute: {exc}")
        raise SystemExit(1)

    # ── 5. Monster attributes ─────────────────────────────────────────────────
    try:
        m = Monster("Goblin", 30, 30, 8, 2, 10)
        assert m.is_alive()
        assert hasattr(m, "reward_gold"), "Monster must have reward_gold attribute"
        assert m.reward_gold == 10
        m.take_damage(30)
        assert not m.is_alive()
        print("✓ Monster attributes and take_damage correct")
    except AssertionError as exc:
        print(f"❌ {exc}")
        raise SystemExit(1)

    # ── 6. Hero extra attributes ──────────────────────────────────────────────
    try:
        h2 = Hero("Zara", 80, 80, 20, 4, "mage", 1)
        assert hasattr(h2, "hero_class"), "Hero must have hero_class attribute"
        assert hasattr(h2, "potions"), "Hero must have potions attribute"
        assert h2.hero_class == "mage"
        assert h2.potions == 1
        print("✓ Hero extra attributes (hero_class, potions) correct")
    except AssertionError as exc:
        print(f"❌ {exc}")
        raise SystemExit(1)

    # ── 7. build_roster ───────────────────────────────────────────────────────
    try:
        roster = build_roster()
        assert isinstance(roster, list), "build_roster() must return a list"
        assert len(roster) >= 3, f"build_roster() must return ≥3 characters, got {len(roster)}"
        heroes = [c for c in roster if isinstance(c, Hero)]
        monsters = [c for c in roster if isinstance(c, Monster)]
        assert len(heroes) >= 1, "Roster must contain at least 1 Hero"
        assert len(monsters) >= 1, "Roster must contain at least 1 Monster"
        for c in roster:
            assert isinstance(c, Character), f"{c!r} is not a Character"
        print(f"✓ build_roster() returns {len(roster)} characters ({len(heroes)} heroes, {len(monsters)} monsters)")
    except AssertionError as exc:
        print(f"❌ {exc}")
        raise SystemExit(1)
    except NotImplementedError:
        print("❌ build_roster() not implemented")
        raise SystemExit(1)

    # ── 8. print_roster produces output ──────────────────────────────────────
    try:
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_roster(roster)
        output = buf.getvalue()
        assert len(output.strip()) > 0, "print_roster() produced no output"
        lines = [ln for ln in output.strip().splitlines() if ln.strip()]
        assert len(lines) >= len(roster), (
            f"print_roster() should print at least one line per character "
            f"(expected ≥{len(roster)}, got {len(lines)})"
        )
        print(f"✓ print_roster() prints {len(lines)} lines")
    except AssertionError as exc:
        print(f"❌ {exc}")
        raise SystemExit(1)
    except NotImplementedError:
        print("❌ print_roster() not implemented")
        raise SystemExit(1)

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("01_arena_roster")
    print()
    print("✅ Project 01 complete: Arena Roster is ready for battle!")
    print()
    print("   You designed Character, Hero, and Monster from scratch.")
    print("   That is object-oriented thinking in action.")


if __name__ == "__main__":
    main()
