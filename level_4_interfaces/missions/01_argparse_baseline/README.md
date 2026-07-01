# Mission 01: argparse Baseline

## Goal

Add CLI arguments to the game so it can be started without interactive prompts:

```bash
python game.py new-game --name Ada --class warrior
python game.py simulate --battles 10
python game.py status
```

## You will learn

- What a CLI interface is and why it matters
- `argparse` from the standard library: subcommands, flags, defaults
- The difference between a command (verb) and an option (--flag)
- Why interactive `input()` makes a program impossible to automate

## Game problem

The starter RPG always asks questions: `Hero name:`, `Choose class:`, `Action [a/p]:`. This is fine for a human player, but it means:

- You cannot run the game from a script
- You cannot test it without pressing keys
- You cannot automate a simulation

A CLI interface separates **what the user wants** (passed as arguments) from **what the program does** (game logic). Once the arguments are parsed, the rest of the code never touches `input()` for startup decisions.

## Python concept

`argparse` is Python's standard library module for parsing command-line arguments.

```python
import argparse

parser = argparse.ArgumentParser(description="RPG game")
subparsers = parser.add_subparsers(dest="command")

# Define a subcommand
new_game = subparsers.add_parser("new-game", help="Start a new game")
new_game.add_argument("--name", default="Hero", help="Hero name")
new_game.add_argument("--class", dest="hero_class", default="warrior",
                      choices=["warrior", "mage", "rogue"])

args = parser.parse_args()
if args.command == "new-game":
    print(f"Starting game as {args.name} ({args.hero_class})")
```

Key concepts:
- **subcommand** (`new-game`, `simulate`, `status`) — what action to take
- **`--flag`** — an optional argument with a value
- **`choices=`** — limits valid values, shows them in `--help`
- **`dest=`** — renames the attribute (needed when the flag has a `-`)

## Your task

Open `task.py`. The game logic is already imported. Your job is the interface layer only.

Implement:

1. **`make_parser() -> argparse.ArgumentParser`** — build the argument parser with three subcommands:
   - `new-game --name NAME --class CLASS` (class choices: warrior / mage / rogue)
   - `simulate --battles N` (default 5)
   - `status` (no arguments)

2. **`cmd_new_game(args)` / `cmd_simulate(args)` / `cmd_status()`** — implement the three command handlers

3. **`main()`** — parse args, dispatch to the right handler; if no subcommand given, print help and exit with code 1

## Run

```bash
uv run python level_4_interfaces/missions/01_argparse_baseline/task.py new-game --name Ada --class warrior
uv run python level_4_interfaces/missions/01_argparse_baseline/task.py simulate --battles 3
uv run python level_4_interfaces/missions/01_argparse_baseline/task.py status
uv run python level_4_interfaces/missions/01_argparse_baseline/task.py --help
```

## Check

```bash
uv run python level_4_interfaces/missions/01_argparse_baseline/check.py
```

## Break it on purpose

Run:

```bash
uv run python level_4_interfaces/missions/01_argparse_baseline/task.py new-game --class wizard
```

argparse should reject `wizard` (not in choices) and print an error automatically. You did not write that validation — `choices=` did it for you.

## Fix it

`--class warrior` is a valid class. The error disappears.

## Side quest

Add `--potions N` to `new-game` (default 3, min 0, max 9). Use `type=int` and write a custom validator that calls `parser.error("--potions must be between 0 and 9")` if the value is out of range.

## Real-world translation

`argparse` is what powers most Python CLI tools you already use: `pip`, `ruff`, `pytest`. They all parse `argv` the same way and dispatch to subcommand handlers — exactly what you just built.

## Checklist

- [ ] `make_parser()` returns a parser with three subcommands
- [ ] `--class` only accepts warrior / mage / rogue; argparse rejects anything else
- [ ] Running with no subcommand prints help and exits with code 1
- [ ] `simulate --battles N` runs N battles without any `input()` prompts
- [ ] `status` prints save file info without starting a game

---

Next mission: `level_4_interfaces/missions/02_typer_cli/README.md`
