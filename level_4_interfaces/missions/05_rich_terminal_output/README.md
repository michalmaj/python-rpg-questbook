# Mission 05: Rich Terminal Output

## Goal

Replace unstructured `print()` output with Rich tables and panels — not for decoration, but to make information **easier to understand at a glance**:

```
# before: walls of undifferentiated text
--- Ada | HP: 96/120 | Gold: 30 | Potions: 2 ---

# after: structured, readable output
┌──────────────────┬───────────────┐
│ Ada              │ HP  96 / 120  │
│ Warrior          │ ⚔  Gold  30   │
│ Potions: 2  ●●○  │ W/L  3 / 1   │
└──────────────────┴───────────────┘
```

## You will learn

- `Console` — the Rich output object (replaces `print()` for formatted output)
- `Table` — display data in aligned columns
- `Panel` — wrap a block of text in a border with a title
- `Text` with styles — bold, colour, and semantic markup
- Why "pretty output" is valuable only when it makes information clearer

## Game problem

The current game prints everything as plain strings. HP, gold, wins, and potions sit in one line, same weight, same colour. A combat result looks the same as a navigation menu. Players scan the output instead of reading it.

Rich solves this by giving each kind of information a visual form:
- **Tables** for structured data (hero stats, monster comparison)
- **Panels** for distinct messages (victory, defeat, save confirmation)
- **Color and style** only to mark *meaning* (green = good, red = danger)

> **The rule:** add colour and formatting only when it makes information easier to understand. "Looks cool" is not a reason. "Makes HP status immediately readable without counting characters" is.

## Python concept

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

# table
table = Table(title="Hero Stats")
table.add_column("Name")
table.add_column("HP", justify="right")
table.add_row("Ada", "96 / 120")
console.print(table)

# panel with styled text
result = Text("Victory!", style="bold green")
console.print(Panel(result, title="Combat Result", border_style="green"))
```

`Console` is Rich's equivalent of `print()` — it handles formatting, colour codes, and terminal width automatically. Always use one shared `Console` instance per module.

## Your task

Open `task.py`. A `console = Console()` is already defined.

Implement:

1. **`show_hero_stats(hero: Hero) -> None`** — display hero stats as a `Table` with two columns: stat name and value. Include name, class, HP (current/max), gold, potions, and win/loss record.

2. **`show_combat_start(hero: Hero, monster: Monster) -> None`** — print a `Panel` announcing the battle. Title: `"⚔ Battle"`. Body: hero name vs monster name, plus both HP values.

3. **`show_combat_result(winner: str, gold_gained: int = 0) -> None`** — print a `Panel` for victory (green border) or defeat (red border). `winner` is either `"hero"` or `"monster"`.

4. **`show_error(message: str) -> None`** — print the error message to `console.print(..., style="bold red")`. Use `stderr=True` so it goes to stderr, not stdout.

## Run

```bash
uv run python level_4_interfaces/missions/05_rich_terminal_output/task.py
```

## Check

```bash
uv run python level_4_interfaces/missions/05_rich_terminal_output/check.py
```

## Break it on purpose

Remove `stderr=True` from `show_error()`. Pipe stdout to `/dev/null`:

```bash
uv run python level_4_interfaces/missions/05_rich_terminal_output/task.py 2>/dev/null
```

The error message disappears — it went to stdout, which you discarded. With `stderr=True`, the error appears even when stdout is redirected.

## Fix it

Add `stderr=True` back. Error messages go to stderr again.

## Side quest

Add a `show_simulation_progress(battles: int)` function that uses `rich.progress.track()` to display a progress bar while simulating battles:

```python
from rich.progress import track

for _ in track(range(battles), description="Simulating..."):
    simulate_one_battle(hero, monster)
```

## Real-world translation

`rich` is used by tools like `pytest`, `pip`, `Textual`, and Typer itself. When you see coloured output in `pytest` or the pip progress bar, you are looking at Rich. The `Console` object is the same across all of them. Rich is the standard way to produce readable terminal output in modern Python.

## Checklist

- [ ] `console = Console()` is at module level (one shared instance)
- [ ] `show_hero_stats()` uses `Table` with at least name, HP, gold, potions, W/L
- [ ] `show_combat_start()` uses `Panel` to announce the battle
- [ ] `show_combat_result()` uses green/red border to distinguish win from loss
- [ ] `show_error()` uses `stderr=True` — errors go to stderr, not stdout
- [ ] No `print()` calls for the four functions above — all go through `console`

---

Next mission: `level_4_interfaces/missions/06_session_reports/README.md`
