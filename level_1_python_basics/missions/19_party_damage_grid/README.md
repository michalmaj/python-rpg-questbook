# Mission 19: Party Damage Grid

## Goal

Read and reduce a 2D array — rows and columns of numbers — and understand
exactly what `axis` means when you do.

## Game problem

Three heroes fought a four-round battle. You have their damage as a grid:
hero rows, round columns. Two questions a game designer would ask:

- How much damage did each hero deal across the whole fight?
- How much damage did the party deal in each round?

Same grid, two different answers, because you're collapsing a different
dimension each time.

## The grid

|         | Round 1 | Round 2 | Round 3 | Round 4 |
|---------|---------|---------|---------|---------|
| Warrior | 12      | 15      | 10      | 18      |
| Mage    | 20      | 5       | 22      | 19      |
| Rogue   | 14      | 14      | 16      | 15      |

## Python concept

A 2D NumPy array is rows of rows. Two new pieces of indexing:

```python
grid = np.array([[1, 2, 3], [4, 5, 6]])
grid[0]      # [1 2 3]  <- the first row
grid[:, 1]   # [2 5]    <- the second column, across every row
```

`grid[0]` picks a row, the same way indexing already worked. `grid[:, 1]`
is new: `:` means "every row," and `1` picks column index 1 out of each.

**Axis** tells an aggregation which dimension to collapse:

- `grid.sum(axis=1)` collapses **across each row** — one result per row.
  On the damage grid, that's "add up all 4 rounds for each hero" → one
  total per hero.
- `grid.sum(axis=0)` collapses **down each column** — one result per
  column. On the damage grid, that's "add up all 3 heroes for each
  round" → one total per round.

The axis you pick is the dimension that *disappears* from the result —
what's left is the answer to your question.

One more thing before you start: adding a plain number to the whole grid
(`grid + 2`) works the same way it did on a 1D array — NumPy stretches the
scalar across every position. This is called **broadcasting**; you'll see
more of it later.

## Your task

Open `task.py`. For each TODO, the expected value is given in a comment —
work out which NumPy call produces it, using what you just read above.

## Run

```bash
uv run python missions/19_party_damage_grid/task.py
```

## Check

```bash
uv run python missions/19_party_damage_grid/check.py
```

---

Next mission: `level_1_python_basics/missions/20_damage_distributions/README.md`
