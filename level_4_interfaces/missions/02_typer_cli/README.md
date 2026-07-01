# Mission 02: Typer CLI

## Goal

Rewrite the argparse CLI from Mission 01 using **Typer** — Python type hints become the CLI contract automatically:

```bash
rpg new-game --name Ada --class warrior
rpg simulate --battles 10
rpg status
```

## You will learn

- How Typer turns type annotations into CLI arguments
- `@app.command()` and `typer.Typer()` for subcommands
- `Annotated` + `typer.Option()` for named flags
- `typer.echo()` and `typer.Exit()` for output and exit codes
- Why type hints as CLI contracts reduce boilerplate vs argparse

## Game problem

The argparse version from M01 works, but it required a lot of plumbing: `add_subparsers`, `add_argument`, `dest=`, `type=int`, explicit `choices=`, manual dispatch in `main()`. The parser definition is verbose and separate from the function signatures.

Typer reads your function's type annotations and generates the parser automatically. The function *is* the command — parameters with `Option()` become `--flags`.

## Python concept

**Typer** builds CLI apps from type-annotated functions.

```python
import typer
from typing import Annotated

app = typer.Typer()

@app.command("new-game")
def new_game(
    name: Annotated[str, typer.Option("--name", help="Hero name")] = "Hero",
    hero_class: Annotated[str, typer.Option("--class", "--hero-class")] = "warrior",
) -> None:
    typer.echo(f"Starting game as {name} ({hero_class})")

if __name__ == "__main__":
    app()
```

Typer generates `--help`, type coercion, and error messages from the annotations. You write a function; Typer builds the CLI.

> **Typer is built on Click.** If you later need lower-level CLI control — custom parameter types, complex group nesting, plugin hooks — Click is the layer directly below Typer and is worth learning.

## Enum as CLI choice

Instead of `choices=["warrior", "mage", "rogue"]`, Typer can use a Python `Enum`:

```python
from enum import Enum

class HeroClass(str, Enum):
    warrior = "warrior"
    mage = "mage"
    rogue = "rogue"

@app.command("new-game")
def new_game(
    hero_class: Annotated[HeroClass, typer.Option("--class")] = HeroClass.warrior,
) -> None:
    ...
```

Typer accepts `--class warrior` and gives you `HeroClass.warrior` — validated, typed, no boilerplate.

## Your task

Open `task.py`. The game helpers are already imported.

Implement:

1. **`app = typer.Typer()`** — create the app at module level

2. **`@app.command("new-game")`** `def new_game(name, hero_class)` — same behaviour as M01's `cmd_new_game`, but using Typer's `Annotated` + `Option()`

3. **`@app.command()`** `def simulate(battles)` — same as M01's `cmd_simulate`, but with `Annotated[int, typer.Option("--battles")]`

4. **`@app.command()`** `def status()` — same as M01's `cmd_status`

5. **`if __name__ == "__main__": app()`** — Typer handles parsing and dispatch

## Run

```bash
uv run python level_4_interfaces/missions/02_typer_cli/task.py new-game --name Ada --class warrior
uv run python level_4_interfaces/missions/02_typer_cli/task.py simulate --battles 3
uv run python level_4_interfaces/missions/02_typer_cli/task.py status
uv run python level_4_interfaces/missions/02_typer_cli/task.py --help
uv run python level_4_interfaces/missions/02_typer_cli/task.py new-game --help
```

## Check

```bash
uv run python level_4_interfaces/missions/02_typer_cli/check.py
```

## Break it on purpose

Run:

```bash
uv run python level_4_interfaces/missions/02_typer_cli/task.py new-game --class wizard
```

Typer (via the Enum) rejects `wizard` and prints:

```
Error: Invalid value for '--class': 'wizard' is not one of ...
```

You did not write that error — the Enum did.

## Fix it

`--class warrior` is valid. Typer accepts it.

## Side quest

Add `--difficulty` to `simulate` as an `Enum` with values `easy / normal / hard`. In `easy` mode, halve monster ATK. In `hard` mode, double it. Typer's Enum support makes this a one-liner addition.

## Real-world translation

Tools like `fastapi`, `sqlmodel`, and many data pipelines use type annotations to generate behaviour automatically. Typer applies the same idea to the CLI layer. After this mission, you have seen the same pattern in Pydantic (data validation), dataclasses (data containers), and now Typer (CLI contracts) — Python's type system is the common thread.

## Checklist

- [ ] `app = typer.Typer()` exists at module level
- [ ] `new-game`, `simulate`, and `status` are registered as Typer commands
- [ ] `--class wizard` is rejected automatically (Enum or choices)
- [ ] `--help` shows all three commands and their flags
- [ ] No manual argument parsing — no `argparse`, no `sys.argv`

---

Next mission: `level_4_interfaces/missions/03_stdlib_logging/README.md`
