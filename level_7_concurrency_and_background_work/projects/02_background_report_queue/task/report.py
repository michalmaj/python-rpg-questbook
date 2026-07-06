"""Report computation from session JSON files.

Pre-implemented — do not modify this file.
compute_report() is called by the background job and returns a plain dict
that gets stored as the job result.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data" / "sessions"


def compute_report(label: str = "combat_report") -> dict:
    """Read all session JSON files and return aggregated stats + Markdown."""
    sessions = []
    for path in sorted(DATA_DIR.glob("*.json")):
        sessions.append(json.loads(path.read_text()))

    if not sessions:
        return {
            "total_sessions": 0,
            "hero_wins": 0,
            "monster_wins": 0,
            "hero_win_rate": 0.0,
            "avg_damage_dealt": 0.0,
            "avg_damage_taken": 0.0,
            "markdown": "# Combat Report\n\nNo sessions found.",
        }

    total = len(sessions)
    hero_wins = sum(1 for s in sessions if s["outcome"] == "hero_win")
    monster_wins = total - hero_wins
    hero_win_rate = round(hero_wins / total, 4)
    avg_dealt = round(sum(s["damage_dealt"] for s in sessions) / total, 2)
    avg_taken = round(sum(s["damage_taken"] for s in sessions) / total, 2)

    markdown = (
        f"# Combat Report: {label}\n\n"
        f"| Metric | Value |\n"
        f"|--------|-------|\n"
        f"| Total sessions | {total} |\n"
        f"| Hero wins | {hero_wins} |\n"
        f"| Monster wins | {monster_wins} |\n"
        f"| Hero win rate | {hero_win_rate:.1%} |\n"
        f"| Avg damage dealt | {avg_dealt} |\n"
        f"| Avg damage taken | {avg_taken} |\n"
    )

    return {
        "total_sessions": total,
        "hero_wins": hero_wins,
        "monster_wins": monster_wins,
        "hero_win_rate": hero_win_rate,
        "avg_damage_dealt": avg_dealt,
        "avg_damage_taken": avg_taken,
        "markdown": markdown,
    }
