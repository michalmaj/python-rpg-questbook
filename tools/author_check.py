"""Author tooling: verify course structure, links, and check.py hygiene.

Run from the repo root:
    uv run python tools/author_check.py

This is not a student tool — it checks the repo for authoring mistakes.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[1]
LEVEL1_ROOT = REPO_ROOT / "level_1_python_basics"
LEVEL2_ROOT = REPO_ROOT / "level_2_oop_and_design"

# ── Level 1 content ───────────────────────────────────────────────────────────

L1_MISSIONS = [
    "01_hero_stats", "02_damage_and_healing", "03_choose_your_hero",
    "04_combat_loop", "05_arena_challenge", "06_hero_inventory",
    "07_monster_dictionary", "08_attack_function", "09_dice_rolls",
    "10_safe_input", "11_combat_log", "12_save_game", "13_split_the_game",
    "14_hero_dataclass", "15_test_the_damage", "16_dice_are_data",
    "17_damage_distributions", "18_read_combat_logs", "19_filter_and_group",
    "20_plot_the_results",
]

L1_PROJECTS = [
    "01_battle_calculator", "02_turn_based_combat", "03_terminal_rpg",
    "04_full_rpg", "05_analytics_report",
]

L1_MISSION_FILE_EXCEPTIONS: dict[str, set[str]] = {
    "15_test_the_damage": {"README.md", "test_combat.py", "check.py"},
}

# ── Level 2 content ───────────────────────────────────────────────────────────

L2_MISSIONS = [
    "01_extract_hero", "02_monster_class", "03_character_base",
    "04_type_hints", "05_enums", "06_properties", "07_dataclasses",
    "08_module_split", "09_pure_functions", "10_add_tests",
]

L2_PROJECTS = [
    "01_refactored_rpg",
]

L2_MISSION_FILE_EXCEPTIONS: dict[str, set[str]] = {
    # M10 uses test_combat.py and combat.py instead of task.py
    "10_add_tests": {"README.md", "test_combat.py", "combat.py", "check.py"},
}

# ── Shared config ─────────────────────────────────────────────────────────────

REQUIRED_MISSION_FILES: set[str] = {"README.md", "task.py", "check.py"}
REQUIRED_PROJECT_FILES: set[str] = {"README.md", "check.py"}

errors: list[str] = []
warnings: list[str] = []
ok: list[str] = []


def check(condition: bool, msg_ok: str, msg_fail: str, warn: bool = False) -> None:
    if condition:
        ok.append(f"  ✓ {msg_ok}")
    elif warn:
        warnings.append(f"  ⚠ {msg_fail}")
    else:
        errors.append(f"  ✗ {msg_fail}")


def check_folder_structure(
    level_root: Path,
    missions: list[str],
    projects: list[str],
    mission_exceptions: dict[str, set[str]],
    label: str,
) -> None:
    for mission_id in missions:
        folder = level_root / "missions" / mission_id
        check(folder.exists(),
              f"{label}/missions/{mission_id}/ exists",
              f"MISSING: {label}/missions/{mission_id}/")
        if folder.exists():
            required = mission_exceptions.get(mission_id, REQUIRED_MISSION_FILES)
            for fname in required:
                fpath = folder / fname
                check(fpath.exists(),
                      f"  {mission_id}/{fname}",
                      f"MISSING: {label}/missions/{mission_id}/{fname}")

    for project_id in projects:
        folder = level_root / "projects" / project_id
        check(folder.exists(),
              f"{label}/projects/{project_id}/ exists",
              f"MISSING: {label}/projects/{project_id}/")
        if folder.exists():
            for fname in REQUIRED_PROJECT_FILES:
                fpath = folder / fname
                check(fpath.exists(),
                      f"  {project_id}/{fname}",
                      f"MISSING: {label}/projects/{project_id}/{fname}")


def check_hygiene(level_root: Path, missions: list[str], projects: list[str]) -> None:
    all_checks = (
        [level_root / "missions" / m / "check.py" for m in missions]
        + [level_root / "projects" / p / "check.py" for p in projects]
    )
    for path in all_checks:
        if not path.exists():
            continue
        text = path.read_text()
        rel = path.relative_to(REPO_ROOT)
        check(
            "raise SystemExit(1)" in text,
            f"{rel}: has SystemExit(1)",
            f"{rel}: MISSING raise SystemExit(1) in except block",
        )
        check(
            '"uv", "run", "python"' not in text,
            f"{rel}: no uv-run-python subprocess",
            f"{rel}: uses ['uv','run','python',...] — change to sys.executable",
        )


# Matches backtick paths for both levels, e.g.
# `level_1_python_basics/missions/02_damage/README.md`
# `level_2_oop_and_design/missions/03_character_base/README.md`
LINK_PATTERN = re.compile(
    r"`(level_(?:1_python_basics|2_oop_and_design)/(?:missions|projects)/[\w/._-]+)`"
)


def check_readme_links(level_root: Path, missions: list[str], projects: list[str], label: str) -> None:
    for mission_id in missions:
        readme = level_root / "missions" / mission_id / "README.md"
        if not readme.exists():
            continue
        for match in LINK_PATTERN.finditer(readme.read_text()):
            target = REPO_ROOT / match.group(1)
            check(
                target.exists(),
                f"  {label}/missions/{mission_id}: link '{match.group(1)}' valid",
                f"  {label}/missions/{mission_id}: BROKEN link '{match.group(1)}'",
            )

    for project_id in projects:
        readme = level_root / "projects" / project_id / "README.md"
        if not readme.exists():
            continue
        for match in LINK_PATTERN.finditer(readme.read_text()):
            target = REPO_ROOT / match.group(1)
            check(
                target.exists(),
                f"  {label}/projects/{project_id}: link '{match.group(1)}' valid",
                f"  {label}/projects/{project_id}: BROKEN link '{match.group(1)}'",
            )


# ── Run all checks ────────────────────────────────────────────────────────────

print("Checking Level 1 folder structure…")
check_folder_structure(LEVEL1_ROOT, L1_MISSIONS, L1_PROJECTS, L1_MISSION_FILE_EXCEPTIONS, "level_1")

print("Checking Level 2 folder structure…")
check_folder_structure(LEVEL2_ROOT, L2_MISSIONS, L2_PROJECTS, L2_MISSION_FILE_EXCEPTIONS, "level_2")

print("Checking check.py hygiene (Level 1)…")
check_hygiene(LEVEL1_ROOT, L1_MISSIONS, L1_PROJECTS)

print("Checking check.py hygiene (Level 2)…")
check_hygiene(LEVEL2_ROOT, L2_MISSIONS, L2_PROJECTS)

print("Checking README next-mission links…")
check_readme_links(LEVEL1_ROOT, L1_MISSIONS, L1_PROJECTS, "level_1")
check_readme_links(LEVEL2_ROOT, L2_MISSIONS, L2_PROJECTS, "level_2")

print("Checking COURSE_MAP.md links…")
course_map = REPO_ROOT / "COURSE_MAP.md"
if course_map.exists():
    for match in re.finditer(r"\(([^)]+\.md)\)", course_map.read_text()):
        target = REPO_ROOT / match.group(1)
        check(
            target.exists(),
            f"COURSE_MAP link '{match.group(1)}' valid",
            f"COURSE_MAP BROKEN link: '{match.group(1)}'",
        )

# ── Report ────────────────────────────────────────────────────────────────────

print()
if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(e)
if warnings:
    print(f"WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(w)

print(f"\n{'✅ All checks passed!' if not errors else '❌ Errors found — see above.'}")
print(f"   {len(ok)} checks passed, {len(errors)} errors, {len(warnings)} warnings.\n")

if errors:
    sys.exit(1)
