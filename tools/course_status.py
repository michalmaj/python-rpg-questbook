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
        ],
        [],
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
