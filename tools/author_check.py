"""Author tooling: verify course structure, links, and check.py hygiene.

Run from the repo root:
    uv run python tools/author_check.py

This is not a student tool — it checks the repo for authoring mistakes.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[1]
LEVEL1_ROOT = REPO_ROOT / "level_1_python_basics"

MISSIONS = [
    "01_hero_stats", "02_damage_and_healing", "03_choose_your_hero",
    "04_combat_loop", "05_arena_challenge", "06_hero_inventory",
    "07_monster_dictionary", "08_attack_function", "09_dice_rolls",
    "10_safe_input", "11_combat_log", "12_save_game", "13_split_the_game",
    "14_hero_dataclass", "15_test_the_damage", "16_dice_are_data",
    "17_damage_distributions", "18_read_combat_logs", "19_filter_and_group",
    "20_plot_the_results",
]

PROJECTS = [
    "01_battle_calculator", "02_turn_based_combat", "03_terminal_rpg",
    "04_full_rpg", "05_analytics_report",
]

REQUIRED_MISSION_FILES = {"README.md", "task.py", "check.py"}
# Exceptions: missions that use a different student file name
MISSION_FILE_EXCEPTIONS: dict[str, set[str]] = {
    "15_test_the_damage": {"README.md", "test_combat.py", "check.py"},
}
REQUIRED_PROJECT_FILES = {"README.md", "check.py"}

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


# ── 1. Folder and file existence ─────────────────────────────────────────────

print("Checking folder structure…")

for mission_id in MISSIONS:
    folder = LEVEL1_ROOT / "missions" / mission_id
    check(folder.exists(), f"missions/{mission_id}/ exists", f"MISSING: missions/{mission_id}/")
    if folder.exists():
        required = MISSION_FILE_EXCEPTIONS.get(mission_id, REQUIRED_MISSION_FILES)
        for fname in required:
            fpath = folder / fname
            check(fpath.exists(), f"  {mission_id}/{fname}", f"MISSING: missions/{mission_id}/{fname}")

for project_id in PROJECTS:
    folder = LEVEL1_ROOT / "projects" / project_id
    check(folder.exists(), f"projects/{project_id}/ exists", f"MISSING: projects/{project_id}/")
    if folder.exists():
        for fname in REQUIRED_PROJECT_FILES:
            fpath = folder / fname
            check(fpath.exists(), f"  {project_id}/{fname}", f"MISSING: projects/{project_id}/{fname}")

# ── 2. check.py hygiene ──────────────────────────────────────────────────────

print("Checking check.py hygiene…")

all_checks = (
    [LEVEL1_ROOT / "missions" / m / "check.py" for m in MISSIONS]
    + [LEVEL1_ROOT / "projects" / p / "check.py" for p in PROJECTS]
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

# ── 3. README next-links ─────────────────────────────────────────────────────

print("Checking README next-mission links…")

import re

LINK_PATTERN = re.compile(r"`(level_1_python_basics/(?:missions|projects)/[\w/._-]+)`")

for mission_id in MISSIONS:
    readme = LEVEL1_ROOT / "missions" / mission_id / "README.md"
    if not readme.exists():
        continue
    text = readme.read_text()
    for match in LINK_PATTERN.finditer(text):
        target = REPO_ROOT / match.group(1)
        check(
            target.exists(),
            f"  missions/{mission_id}: link '{match.group(1)}' valid",
            f"  missions/{mission_id}: BROKEN link '{match.group(1)}'",
        )

for project_id in PROJECTS:
    readme = LEVEL1_ROOT / "projects" / project_id / "README.md"
    if not readme.exists():
        continue
    text = readme.read_text()
    for match in LINK_PATTERN.finditer(text):
        target = REPO_ROOT / match.group(1)
        check(
            target.exists(),
            f"  projects/{project_id}: link '{match.group(1)}' valid",
            f"  projects/{project_id}: BROKEN link '{match.group(1)}'",
        )

# ── 4. COURSE_MAP links ──────────────────────────────────────────────────────

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

# ── Report ───────────────────────────────────────────────────────────────────

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
