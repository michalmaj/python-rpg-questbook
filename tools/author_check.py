"""Author tooling: verify course structure, links, and check.py hygiene.

Run from the repo root:
    uv run python tools/author_check.py

This is not a student tool — it checks the repo for authoring mistakes.
"""

import re
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).parents[1]
LEVEL1_ROOT = REPO_ROOT / "level_1_python_basics"
LEVEL2_ROOT = REPO_ROOT / "level_2_oop_and_design"
LEVEL3_ROOT = REPO_ROOT / "level_3_validation_and_persistence"
LEVEL4_ROOT = REPO_ROOT / "level_4_interfaces"
LEVEL5_ROOT = REPO_ROOT / "level_5_maintainability"
LEVEL6_ROOT = REPO_ROOT / "level_6_api"
LEVEL7_ROOT = REPO_ROOT / "level_7_concurrency_and_background_work"

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
    "01_arena_roster", "02_character_sheet_builder", "03_refactored_rpg",
]

L2_MISSION_FILE_EXCEPTIONS: dict[str, set[str]] = {
    # M10 uses test_combat.py and combat.py instead of task.py
    "10_add_tests": {"README.md", "test_combat.py", "combat.py", "check.py"},
}

# ── Level 3 content ───────────────────────────────────────────────────────────

L3_MISSIONS = [
    "01_external_data_is_untrusted", "02_pydantic_monster_config",
    "03_load_game_catalogs", "04_save_and_load_game_json",
    "05_repository_pattern", "06_combat_log_repository", "07_settings_and_paths",
]

L3_PROJECTS = [
    "01_validated_bestiary", "02_save_slot_manager", "03_sqlite_repository_backend",
]

L3_MISSION_FILE_EXCEPTIONS: dict[str, set[str]] = {}

# ── Level 4 content ───────────────────────────────────────────────────────────

L4_MISSIONS = [
    "01_argparse_baseline", "02_typer_cli", "03_stdlib_logging",
    "04_log_files", "05_rich_terminal_output", "06_session_reports",
]

L4_PROJECTS = [
    "01_quest_master_cli", "02_observable_battle_runner", "03_installable_cli_tool",
]

L4_MISSION_FILE_EXCEPTIONS: dict[str, set[str]] = {}

# ── Level 5 content ───────────────────────────────────────────────────────────

L5_MISSIONS = [
    "01_ruff_linting", "02_mypy_type_checking", "03_pyright_strict",
    "04_pytest_fixtures", "05_pytest_parametrize", "06_coverage",
    "07_error_handling", "08_pre_commit", "09_github_actions_ci",
]

L5_PROJECTS = [
    "01_quality_gate_rescue", "02_combat_regression_suite", "03_full_release_pipeline",
]

L5_MISSION_FILE_EXCEPTIONS: dict[str, set[str]] = {
    # M04-M06 use rpg.py + conftest.py + test_combat.py instead of task.py
    "04_pytest_fixtures": {"README.md", "rpg.py", "conftest.py", "test_combat.py", "check.py"},
    "05_pytest_parametrize": {"README.md", "rpg.py", "conftest.py", "test_combat.py", "check.py"},
    "06_coverage": {"README.md", "rpg.py", "conftest.py", "test_combat.py", "pyproject.toml", "check.py"},
}

# ── Level 6 content ───────────────────────────────────────────────────────────

L6_MISSIONS = [
    "01_first_fastapi_app", "02_request_response_schemas",
    "03_routes_call_services", "04_api_routers",
    "05_dependencies_and_repositories", "06_api_errors_and_status_codes",
    "07_api_tests", "08_openapi_and_api_polish",
]

L6_PROJECTS = [
    "01_battle_preview_api", "02_monster_catalog_api", "03_rpg_battle_api",
]

L6_MISSION_FILE_EXCEPTIONS: dict[str, set[str]] = {
    # M01-M03: task.py + rpg/ subpackage (pre-written service)
    "01_first_fastapi_app": {"README.md", "task.py", "check.py", "rpg/__init__.py"},
    "02_request_response_schemas": {"README.md", "task.py", "check.py", "rpg/__init__.py"},
    "03_routes_call_services": {"README.md", "task.py", "check.py", "rpg/__init__.py"},
    # M04-M08: task/ package pattern
    "04_api_routers": {"README.md", "check.py", "task/__init__.py", "task/config.py"},
    "05_dependencies_and_repositories": {"README.md", "check.py", "task/__init__.py", "task/config.py"},
    "06_api_errors_and_status_codes": {"README.md", "check.py", "task/__init__.py", "task/config.py"},
    "07_api_tests": {"README.md", "check.py", "task/__init__.py", "task/config.py"},
    "08_openapi_and_api_polish": {"README.md", "check.py", "task/__init__.py", "task/config.py"},
}

# ── Level 7 content ───────────────────────────────────────────────────────────

L7_MISSIONS = [
    "01_blocking_vs_background_work",
    "02_asyncio_basics",
    "03_async_api_endpoints",
    "04_background_jobs",
    "05_job_status_repository",
    "06_thread_pool_for_blocking_io",
    "07_process_pool_for_cpu_work",
    "08_testing_background_work",
]

L7_PROJECTS = [
    "01_async_quest_aggregator",
    "02_background_report_queue",
    "03_concurrent_tournament_runner",
]

L7_MISSION_FILE_EXCEPTIONS: dict[str, set[str]] = {
    # task/ package missions (no task.py at top level)
    "03_async_api_endpoints": {"README.md", "check.py", "task/__init__.py"},
    "04_background_jobs": {"README.md", "check.py", "task/__init__.py"},
    "05_job_status_repository": {"README.md", "check.py", "task/__init__.py"},
    "08_testing_background_work": {"README.md", "check.py", "task/__init__.py"},
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


# Matches backtick paths for all levels, e.g.
# `level_1_python_basics/missions/02_damage/README.md`
# `level_3_validation_and_persistence/missions/01_external_data_is_untrusted/README.md`
LINK_PATTERN = re.compile(
    r"`(level_(?:1_python_basics|2_oop_and_design|3_validation_and_persistence"
    r"|4_interfaces|5_maintainability|6_api|7_concurrency_and_background_work)"
    r"/(?:missions|projects)/[\w/._-]+)`"
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


def check_dependencies() -> None:
    """Verify pyproject.toml contains dependencies required by each level."""
    pyproject = REPO_ROOT / "pyproject.toml"
    if not pyproject.exists():
        errors.append("  ✗ pyproject.toml not found")
        return
    with pyproject.open("rb") as f:
        data = tomllib.load(f)
    deps: list[str] = data.get("project", {}).get("dependencies", [])
    dep_names = {re.split(r"[\[>=<!]", d)[0].strip().lower() for d in deps}

    if LEVEL3_ROOT.exists():
        for required in ("pydantic", "pydantic-settings"):
            check(
                required.lower() in dep_names,
                f"pyproject.toml: '{required}' listed (required by Level 3)",
                f"pyproject.toml: MISSING '{required}' — Level 3 imports it",
            )

    if LEVEL4_ROOT.exists():
        for required in ("typer", "rich"):
            check(
                required.lower() in dep_names,
                f"pyproject.toml: '{required}' listed (required by Level 4)",
                f"pyproject.toml: MISSING '{required}' — Level 4 imports it",
            )

    if LEVEL5_ROOT.exists():
        dev_deps: list[str] = data.get("dependency-groups", {}).get("dev", [])
        dev_dep_names = {re.split(r"[>=<!]", d)[0].strip().lower() for d in dev_deps}
        for required in ("mypy", "pyright", "pytest-cov"):
            check(
                required.lower() in dev_dep_names,
                f"pyproject.toml dev: '{required}' listed (required by Level 5)",
                f"pyproject.toml dev: MISSING '{required}' — Level 5 needs it",
            )

    if LEVEL6_ROOT.exists():
        for required in ("fastapi", "httpx"):
            check(
                required.lower() in dep_names,
                f"pyproject.toml: '{required}' listed (required by Level 6)",
                f"pyproject.toml: MISSING '{required}' — Level 6 imports it",
            )


# ── Run all checks ────────────────────────────────────────────────────────────

print("Checking Level 1 folder structure…")
check_folder_structure(LEVEL1_ROOT, L1_MISSIONS, L1_PROJECTS, L1_MISSION_FILE_EXCEPTIONS, "level_1")

print("Checking Level 2 folder structure…")
check_folder_structure(LEVEL2_ROOT, L2_MISSIONS, L2_PROJECTS, L2_MISSION_FILE_EXCEPTIONS, "level_2")

print("Checking Level 3 folder structure…")
check_folder_structure(LEVEL3_ROOT, L3_MISSIONS, L3_PROJECTS, L3_MISSION_FILE_EXCEPTIONS, "level_3")

print("Checking Level 4 folder structure…")
check_folder_structure(LEVEL4_ROOT, L4_MISSIONS, L4_PROJECTS, L4_MISSION_FILE_EXCEPTIONS, "level_4")

print("Checking Level 5 folder structure…")
check_folder_structure(LEVEL5_ROOT, L5_MISSIONS, L5_PROJECTS, L5_MISSION_FILE_EXCEPTIONS, "level_5")

print("Checking Level 6 folder structure…")
check_folder_structure(LEVEL6_ROOT, L6_MISSIONS, L6_PROJECTS, L6_MISSION_FILE_EXCEPTIONS, "level_6")

print("Checking Level 7 folder structure…")
check_folder_structure(LEVEL7_ROOT, L7_MISSIONS, L7_PROJECTS, L7_MISSION_FILE_EXCEPTIONS, "level_7")

print("Checking check.py hygiene (Level 1)…")
check_hygiene(LEVEL1_ROOT, L1_MISSIONS, L1_PROJECTS)

print("Checking check.py hygiene (Level 2)…")
check_hygiene(LEVEL2_ROOT, L2_MISSIONS, L2_PROJECTS)

print("Checking check.py hygiene (Level 3)…")
check_hygiene(LEVEL3_ROOT, L3_MISSIONS, L3_PROJECTS)

print("Checking check.py hygiene (Level 4)…")
check_hygiene(LEVEL4_ROOT, L4_MISSIONS, L4_PROJECTS)

print("Checking check.py hygiene (Level 5)…")
check_hygiene(LEVEL5_ROOT, L5_MISSIONS, L5_PROJECTS)

print("Checking check.py hygiene (Level 6)…")
check_hygiene(LEVEL6_ROOT, L6_MISSIONS, L6_PROJECTS)

print("Checking check.py hygiene (Level 7)…")
check_hygiene(LEVEL7_ROOT, L7_MISSIONS, L7_PROJECTS)

print("Checking README next-mission links…")
check_readme_links(LEVEL1_ROOT, L1_MISSIONS, L1_PROJECTS, "level_1")
check_readme_links(LEVEL2_ROOT, L2_MISSIONS, L2_PROJECTS, "level_2")
check_readme_links(LEVEL3_ROOT, L3_MISSIONS, L3_PROJECTS, "level_3")
check_readme_links(LEVEL4_ROOT, L4_MISSIONS, L4_PROJECTS, "level_4")

print("Checking README next-mission links (Level 5)…")
check_readme_links(LEVEL5_ROOT, L5_MISSIONS, L5_PROJECTS, "level_5")

print("Checking README next-mission links (Level 6)…")
check_readme_links(LEVEL6_ROOT, L6_MISSIONS, L6_PROJECTS, "level_6")

print("Checking pyproject.toml dependencies…")
check_dependencies()

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

print("Checking level documentation coverage…")
readme_text = (REPO_ROOT / "README.md").read_text() if (REPO_ROOT / "README.md").exists() else ""
course_map_text = course_map.read_text() if course_map.exists() else ""
_level_checks = [
    (LEVEL1_ROOT, "level_1_python_basics", "Level 1"),
    (LEVEL2_ROOT, "level_2_oop_and_design", "Level 2"),
    (LEVEL3_ROOT, "level_3_validation_and_persistence", "Level 3"),
    (LEVEL4_ROOT, "level_4_interfaces", "Level 4"),
    (LEVEL5_ROOT, "level_5_maintainability", "Level 5"),
    (LEVEL6_ROOT, "level_6_api", "Level 6"),
    (LEVEL7_ROOT, "level_7_concurrency_and_background_work", "Level 7"),
]
for level_root, level_dir, label in _level_checks:
    if not level_root.exists():
        continue
    check(
        level_dir in course_map_text,
        f"COURSE_MAP.md documents {label}",
        f"COURSE_MAP.md is missing {label} ({level_dir}) — add a section for it",
    )
    check(
        level_dir in readme_text,
        f"README.md documents {label}",
        f"README.md is missing {label} ({level_dir}) — add it to the course structure",
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
