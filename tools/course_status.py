import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PROGRESS_FILE = REPO_ROOT / ".progress"

WORLDS = [
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
        [],
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

SYMBOLS = {
    "complete": "✓",
    "in_progress": "~",
    "not_started": " ",
}


def load_progress() -> dict:
    if not PROGRESS_FILE.exists():
        return {"missions": {}, "projects": {}}
    return json.loads(PROGRESS_FILE.read_text())


def main() -> None:
    progress = load_progress()
    missions_progress = progress.get("missions", {})
    projects_progress = progress.get("projects", {})

    print()
    print("Python RPG Questbook — Your Progress")
    print("=" * 40)

    next_up = None

    for world_name, missions, projects in WORLDS:
        print()
        print(world_name)
        print()

        for mission_id, mission_name in missions:
            status = missions_progress.get(mission_id, "not_started")
            symbol = SYMBOLS[status]
            print(f"  [{symbol}] {mission_name}")
            if status != "complete" and next_up is None:
                next_up = f"missions/{mission_id}/README.md"

        for project_id, project_name in projects:
            status = projects_progress.get(project_id, "not_started")
            symbol = SYMBOLS[status]
            print(f"  [{symbol}] {project_name}")
            if status != "complete" and next_up is None:
                next_up = f"projects/{project_id}/README.md"

    print()
    if next_up:
        print(f"Next up: {next_up}")
    else:
        print("All worlds complete! Open COURSE_MAP.md for what's next.")
    print()


if __name__ == "__main__":
    main()
