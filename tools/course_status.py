import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
LEVEL1_ROOT = REPO_ROOT / "level_1_python_basics"
LEVEL2_ROOT = REPO_ROOT / "level_2_oop_and_design"
LEVEL3_ROOT = REPO_ROOT / "level_3_validation_and_persistence"
LEVEL4_ROOT = REPO_ROOT / "level_4_interfaces"

LEVEL1_PROGRESS_FILE = LEVEL1_ROOT / ".progress"
LEVEL2_PROGRESS_FILE = LEVEL2_ROOT / ".progress"
LEVEL3_PROGRESS_FILE = LEVEL3_ROOT / ".progress"
LEVEL4_PROGRESS_FILE = LEVEL4_ROOT / ".progress"

LEVEL1_WORLDS = [
    (
        "World 1: First Hero",
        [
            ("01_hero_stats", "Mission 01: Hero Stats"),
            ("02_damage_and_healing", "Mission 02: Damage and Healing"),
            ("03_choose_your_hero", "Mission 03: Choose Your Hero"),
        ],
        [
            ("01_battle_calculator", "Project 01: Battle Calculator"),
        ],
    ),
    (
        "World 2: Combat Logic",
        [
            ("04_combat_loop", "Mission 04: Combat Loop"),
            ("05_arena_challenge", "Mission 05: Arena Challenge"),
            ("06_hero_inventory", "Mission 06: Hero Inventory"),
        ],
        [
            ("02_turn_based_combat", "Project 02: Turn-Based Combat"),
        ],
    ),
    (
        "World 3: Character Data",
        [
            ("07_monster_dictionary", "Mission 07: Monster Dictionary"),
            ("08_attack_function", "Mission 08: Attack Function"),
            ("09_dice_rolls", "Mission 09: Dice Rolls"),
            ("10_safe_input", "Mission 10: Safe Input"),
        ],
        [
            ("03_terminal_rpg", "Project 03: Terminal RPG"),
        ],
    ),
    (
        "World 4: Saving and Structure",
        [
            ("11_combat_log", "Mission 11: Combat Log"),
            ("12_save_game", "Mission 12: Save Game"),
            ("13_split_the_game", "Mission 13: Split the Game"),
            ("14_hero_dataclass", "Mission 14: Hero Dataclass"),
            ("15_test_the_damage", "Mission 15: Test the Damage"),
        ],
        [
            ("04_full_rpg", "Project 04: Full Terminal RPG"),
        ],
    ),
    (
        "Part 2: Game Data Analysis",
        [
            ("16_dice_are_data", "Mission 16: Dice Are Data"),
            ("17_damage_distributions", "Mission 17: Damage Distributions"),
            ("18_read_combat_logs", "Mission 18: Read Combat Logs"),
            ("19_filter_and_group", "Mission 19: Filter and Group"),
            ("20_plot_the_results", "Mission 20: Plot the Results"),
        ],
        [
            ("05_analytics_report", "Project 05: Game Analytics Report"),
        ],
    ),
]

LEVEL2_WORLDS = [
    (
        "World 1: Objects",
        [
            ("01_extract_hero", "Mission 01: Extract Hero"),
            ("02_monster_class", "Mission 02: Monster Class"),
            ("03_character_base", "Mission 03: Character Base"),
        ],
        [],
    ),
    (
        "World 2: Design",
        [
            ("04_type_hints", "Mission 04: Type Hints"),
            ("05_enums", "Mission 05: Enums"),
            ("06_properties", "Mission 06: Properties"),
            ("07_dataclasses", "Mission 07: Dataclasses"),
        ],
        [],
    ),
    (
        "World 3: Structure",
        [
            ("08_module_split", "Mission 08: Module Split"),
            ("09_pure_functions", "Mission 09: Pure Functions"),
            ("10_add_tests", "Mission 10: Add Tests"),
        ],
        [
            ("01_refactored_rpg", "Project 01: Refactored RPG"),
        ],
    ),
]

LEVEL3_WORLDS = [
    (
        "World 1: Trusted Data",
        [
            ("01_external_data_is_untrusted", "Mission 01: External Data Is Untrusted"),
            ("02_pydantic_monster_config", "Mission 02: Pydantic Monster Config"),
            ("03_load_game_catalogs", "Mission 03: Load Game Catalogs"),
        ],
        [],
    ),
    (
        "World 2: Persistence",
        [
            ("04_save_and_load_game_json", "Mission 04: Save and Load Game JSON"),
            ("05_repository_pattern", "Mission 05: Repository Pattern"),
        ],
        [],
    ),
    (
        "World 3: Integration",
        [
            ("06_combat_log_repository", "Mission 06: Combat Log Repository"),
            ("07_settings_and_paths", "Mission 07: Settings and Paths"),
        ],
        [
            ("01_sqlite_repository_backend", "Boss Fight: SQLite Repository Backend"),
        ],
    ),
]

LEVEL4_WORLDS = [
    (
        "World 1: Command Line Interface",
        [
            ("01_argparse_baseline", "Mission 01: argparse Baseline"),
            ("02_typer_cli", "Mission 02: Typer CLI"),
        ],
        [],
    ),
    (
        "World 2: Logging and Observability",
        [
            ("03_stdlib_logging", "Mission 03: stdlib logging"),
            ("04_log_files", "Mission 04: Log Files"),
        ],
        [],
    ),
    (
        "World 3: User-Facing Output",
        [
            ("05_rich_terminal_output", "Mission 05: Rich Terminal Output"),
            ("06_session_reports", "Mission 06: Session Reports"),
        ],
        [
            ("01_installable_cli_tool", "Boss Fight: Installable CLI Tool"),
        ],
    ),
]

SYMBOLS = {
    "complete": "✓",
    "in_progress": "~",
    "not_started": " ",
}


def load_progress(progress_file: Path) -> dict:
    if not progress_file.exists():
        return {"missions": {}, "projects": {}}
    try:
        return json.loads(progress_file.read_text())
    except json.JSONDecodeError:
        print(f"Warning: {progress_file.name} is corrupted. Starting from empty progress.")
        return {"missions": {}, "projects": {}}


def print_level(
    level_name: str,
    worlds: list,
    progress: dict,
    level_prefix: str,
    next_up_ref: list,
) -> None:
    print()
    print(level_name)
    print("─" * 40)

    missions_progress = progress.get("missions", {})
    projects_progress = progress.get("projects", {})

    for world_name, missions, projects in worlds:
        print()
        print(f"  {world_name}")
        print()

        for mission_id, mission_name in missions:
            status = missions_progress.get(mission_id, "not_started")
            symbol = SYMBOLS[status]
            print(f"    [{symbol}] {mission_name}")
            if status != "complete" and not next_up_ref[0]:
                next_up_ref[0] = f"{level_prefix}/missions/{mission_id}/README.md"

        for project_id, project_name in projects:
            status = projects_progress.get(project_id, "not_started")
            symbol = SYMBOLS[status]
            print(f"    [{symbol}] {project_name}")
            if status != "complete" and not next_up_ref[0]:
                next_up_ref[0] = f"{level_prefix}/projects/{project_id}/README.md"


def main() -> None:
    l1_progress = load_progress(LEVEL1_PROGRESS_FILE)
    l2_progress = load_progress(LEVEL2_PROGRESS_FILE)
    l3_progress = load_progress(LEVEL3_PROGRESS_FILE)
    l4_progress = load_progress(LEVEL4_PROGRESS_FILE)

    print()
    print("Python RPG Questbook — Your Progress")
    print("=" * 40)

    next_up: list[str | None] = [None]

    print_level("Level 1: Python Basics", LEVEL1_WORLDS, l1_progress,
                "level_1_python_basics", next_up)
    print_level("Level 2: OOP and Design", LEVEL2_WORLDS, l2_progress,
                "level_2_oop_and_design", next_up)
    print_level("Level 3: Validation and Persistence", LEVEL3_WORLDS, l3_progress,
                "level_3_validation_and_persistence", next_up)
    print_level("Level 4: Interfaces and Reports", LEVEL4_WORLDS, l4_progress,
                "level_4_interfaces", next_up)

    print()
    if next_up[0]:
        print(f"Next up: {next_up[0]}")
    else:
        print("All levels complete! Open COURSE_MAP.md for what's next.")
    print()


if __name__ == "__main__":
    main()
