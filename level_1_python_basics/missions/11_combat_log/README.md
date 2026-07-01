# Mission 11: Combat Log

## Goal

Save combat data to a file so it can be read, shared, and analyzed later.

## You will learn

- `open(filename, mode)` — open a file for reading or writing
- `with` statement — automatically closes the file when done
- `f.write(string)` — write a string to the file
- CSV format — comma-separated values, readable by spreadsheets and Python

## Game problem

After every battle, the game should save a log so you can review what happened.
CSV is the perfect format — simple, widely supported, and ready for analysis in Part 2.

## Your task

Open `task.py`. The combat data is already stored in `combat_log` (a list of dicts from Mission 04).
Write it to `combat_log.csv` with a header row and one row per round.

**How to write a file:**

```python
with open("combat_log.csv", "w") as f:
    f.write("round,hero_hp,monster_hp\n")   # header — \n ends the line
    for entry in combat_log:
        f.write(f"{entry['round']},{entry['hero_hp']},{entry['monster_hp']}\n")
```

`with open(...) as f:` is called a context manager.
It opens the file, runs your code, then closes the file automatically — even if an error occurs.

**The required output file** (`combat_log.csv`):
```
round,hero_hp,monster_hp,hero_dmg,monster_dmg
1,88,45,15,12
2,76,30,15,12
3,64,15,15,12
4,52,0,15,12
```

## Run

```bash
uv run python missions/11_combat_log/task.py
```

Then check the file was created:
```bash
cat combat_log.csv
```

## Check

```bash
uv run python missions/11_combat_log/check.py
```

## Side quest

Read the file back and print it:

```python
with open("combat_log.csv", "r") as f:
    for line in f:
        print(line.strip())
```

`"r"` mode opens for reading. Try it — you'll use this pattern constantly in Part 2.

---

Next mission: `level_1_python_basics/missions/12_save_game/README.md`
