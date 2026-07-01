"""
Mission 06: Session Reports

When the session ends, the game prints "Goodbye!" and the player has no record
of what happened. This mission generates two report files:

    reports/session_2026-07-01_1530.json   ← machine-readable
    reports/session_2026-07-01_1530.md     ← human-readable

Your task:
1. Implement SessionSummary.to_markdown()
2. Implement generate_json_report()
3. Implement generate_md_report()
4. Implement generate_reports() — builds filenames, calls both generators
"""

import random
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field

REPORTS_DIR = Path(__file__).parent / "reports"


# ----- Pydantic report model -------------------------------------------------


class SessionSummary(BaseModel):
    """One play session — validated on creation, serializes to JSON or Markdown."""

    started_at: datetime
    hero_name: str
    hero_class: str
    battles: int = Field(ge=0)
    wins: int = Field(ge=0)
    losses: int = Field(ge=0)
    gold_earned: int = Field(ge=0)
    final_hp: int = Field(ge=0)
    max_hp: int = Field(gt=0)

    def to_json(self) -> str:
        """Serialize to pretty JSON. Use this for machine-readable output."""
        return self.model_dump_json(indent=2)

    def to_markdown(self) -> str:
        # TODO: return a Markdown string with at minimum:
        # - A heading with the hero name
        # - Date from started_at (use .strftime("%Y-%m-%d %H:%M"))
        # - Hero class
        # - Battles, wins, losses
        # - Gold earned
        # - Final HP / max HP
        raise NotImplementedError


# ----- your work: report generators ------------------------------------------


def generate_json_report(session: SessionSummary, path: Path) -> None:
    # TODO:
    # 1. path.parent.mkdir(parents=True, exist_ok=True)
    # 2. path.write_text(session.to_json(), encoding="utf-8")
    raise NotImplementedError


def generate_md_report(session: SessionSummary, path: Path) -> None:
    # TODO:
    # 1. path.parent.mkdir(parents=True, exist_ok=True)
    # 2. path.write_text(session.to_markdown(), encoding="utf-8")
    raise NotImplementedError


def generate_reports(
    session: SessionSummary,
    reports_dir: Path = REPORTS_DIR,
) -> tuple[Path, Path]:
    # TODO:
    # 1. Build timestamp string: session.started_at.strftime("%Y-%m-%d_%H%M")
    # 2. json_path = reports_dir / f"session_{timestamp}.json"
    # 3. md_path   = reports_dir / f"session_{timestamp}.md"
    # 4. Call generate_json_report(session, json_path)
    # 5. Call generate_md_report(session, md_path)
    # 6. Return (json_path, md_path)
    raise NotImplementedError


# ----- demo runner -----------------------------------------------------------


def _run_demo_session() -> SessionSummary:
    """Simulate a short session and return its summary."""
    started = datetime.now()
    monsters = [
        {"name": "Goblin", "gold": 10},
        {"name": "Orc",    "gold": 20},
        {"name": "Troll",  "gold": 40},
    ]
    battles = random.randint(3, 6)
    wins = random.randint(0, battles)
    losses = battles - wins
    gold = sum(
        random.choice(monsters)["gold"] for _ in range(wins)
    )
    return SessionSummary(
        started_at=started,
        hero_name="Ada",
        hero_class="warrior",
        battles=battles,
        wins=wins,
        losses=losses,
        gold_earned=gold,
        final_hp=random.randint(20, 120),
        max_hp=120,
    )


def main() -> None:
    print("Running demo session...")
    session = _run_demo_session()

    try:
        json_path, md_path = generate_reports(session)
    except NotImplementedError:
        print("TODO: implement generate_reports() first.")
        return

    print(f"✓ JSON report: {json_path}")
    print(f"✓ MD  report:  {md_path}")
    print(f"\nSession: {session.battles} battles, {session.wins} wins, {session.gold_earned} gold")


if __name__ == "__main__":
    main()
