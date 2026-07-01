# Mission 06: Session Reports

## Goal

Generate two report files at the end of each play session:

```
reports/
├── session_2026-07-01_1530.json   ← machine-readable (for analysis, piping)
└── session_2026-07-01_1530.md    ← human-readable (for the player)
```

## You will learn

- Pydantic models as report schemas (validate before you write)
- `datetime.now()` and `strftime()` for timestamps
- Two output formats from one data model: JSON for machines, Markdown for humans
- Why separating the data model from its serialization matters

## Game problem

When the session ends, the game prints "Goodbye!" and closes. The player has no record of what happened — how many battles they won, how much gold they earned, or how their hero evolved during the session.

A session report gives the player a record they can:
- Read as a human-readable summary (Markdown)
- Feed to a script or Level 5 analysis tool (JSON)
- Compare between sessions to track progress

## Python concept

**One Pydantic model, two output formats:**

```python
from datetime import datetime
from pydantic import BaseModel

class SessionSummary(BaseModel):
    started_at: datetime
    hero_name: str
    hero_class: str
    battles: int
    wins: int
    losses: int
    gold_earned: int
    final_hp: int
    max_hp: int

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

    def to_markdown(self) -> str:
        return f"""# Session Report

**Hero:** {self.hero_name} ({self.hero_class})
**Date:** {self.started_at.strftime('%Y-%m-%d %H:%M')}

## Combat
- Battles: {self.battles}
- Wins: {self.wins} / Losses: {self.losses}
- Gold earned: {self.gold_earned}
"""
```

The Pydantic model is the single source of truth. `to_json()` writes it for machines. `to_markdown()` formats it for humans. If you add a field, both formats stay in sync automatically.

## Your task

Open `task.py`. `SessionSummary` is defined. Your job is the report generation.

Implement:

1. **`generate_json_report(session: SessionSummary, path: Path) -> None`** — write `session.to_json()` to the file. Create parent directories if needed.

2. **`generate_md_report(session: SessionSummary, path: Path) -> None`** — write `session.to_markdown()` to the file.

3. **`generate_reports(session: SessionSummary, reports_dir: Path) -> tuple[Path, Path]`** — build timestamped filenames, call the two generators, return both paths:

```python
timestamp = session.started_at.strftime("%Y-%m-%d_%H%M")
json_path = reports_dir / f"session_{timestamp}.json"
md_path   = reports_dir / f"session_{timestamp}.md"
```

4. **`SessionSummary.to_markdown()`** — implement the Markdown body. Include: hero name, class, date, battles, wins, losses, gold earned, final HP.

## Run

```bash
uv run python level_4_interfaces/missions/06_session_reports/task.py
```

A simulated session will run and generate two files in `reports/`.

## Check

```bash
uv run python level_4_interfaces/missions/06_session_reports/check.py
```

## Break it on purpose

Remove the `reports_dir.mkdir(parents=True, exist_ok=True)` call. Run the game. You get a `FileNotFoundError` — the directory does not exist yet. The fix is always `mkdir(parents=True, exist_ok=True)` before writing.

## Fix it

Add `mkdir` back. The directory is created before writing.

## Side quest

Add a `battles_detail: list[BattleResult]` field to `SessionSummary`, where `BattleResult` is a small Pydantic model with `monster_name`, `outcome`, and `gold_gained`. Include the battle list in the Markdown report as a table:

```
| Battle | Monster | Outcome | Gold |
|--------|---------|---------|------|
| 1      | Goblin  | win     | 10   |
| 2      | Orc     | loss    | 0    |
```

## Real-world translation

This two-format pattern is common in data pipelines: one canonical data model serializes to JSON for downstream systems and to a human-friendly format (Markdown, HTML, PDF) for reports. Tools like `pytest` do exactly this — the test results are a data model that outputs to the terminal (human) and to `junit.xml` (machines).

## Checklist

- [ ] `generate_json_report()` writes valid JSON and creates parent dirs
- [ ] `generate_md_report()` writes valid Markdown with hero name, battles, wins, losses, gold
- [ ] `generate_reports()` returns `(json_path, md_path)` with timestamped filenames
- [ ] `SessionSummary.to_markdown()` includes all key fields
- [ ] Both files exist after a session run

---

Next: `level_4_interfaces/projects/01_installable_cli_tool/README.md`
