# Mission 06: Hero Inventory

## Goal

Give the hero a bag that can hold multiple items.

## You will learn

- Lists — ordered collections of values
- `append()` — add an item to the end of a list
- `len()` — count how many items are in a list
- `for item in list` — loop directly over a list's contents
- Indexing (`list[0]`, `list[-1]`) — read one item by position
- Slicing (`list[:2]`) — read a range of items as a new list
- Membership (`in`) — check whether something is present

## Game problem

The hero picks up items during the adventure: weapons, potions, scrolls.
We need a way to store them all and loop over them — that's what a list is for.

## Your task

Open `task.py`. The hero already has two starting items.
Add three more, display the full inventory, then read four specific
things out of the finished list: the first item, the last item, the
first two items, and whether a given item is present.

**How lists work:**

```python
inventory = ["sword", "health potion"]   # a list with two strings
inventory.append("shield")               # adds "shield" at the end
print(len(inventory))                    # prints 3
```

**Looping over a list (contrast with Mission 05):**

```python
# Mission 05 — we looped over numbers:
for round_number in range(1, 6):
    ...

# Mission 06 — we loop over the items directly:
for item in inventory:
    print(f"  - {item}")
```

**Reading specific items — indexing, slicing, membership:**

```python
party_names = ["Ada", "Brom", "Kira", "Theron"]

party_names[0]      # "Ada"    — first item
party_names[-1]     # "Theron" — last item, counting from the end
party_names[:2]     # ["Ada", "Brom"] — a new list with the first two items
"Kira" in party_names   # True — is this value present?
```

## Run

```bash
uv run python missions/06_hero_inventory/task.py
```

Expected output:
```
=== Starting Inventory ===
  - sword
  - health potion
=== Updated Inventory ===
  - sword
  - health potion
  - shield
  - magic scroll
  - gold coin

Items carried: 5

First item:  sword
Last item:   gold coin
First two:   ['sword', 'health potion']
Has shield:  True
```

## Check

```bash
uv run python missions/06_hero_inventory/check.py
```

## Side quest

Try removing an item:
```python
inventory.remove("gold coin")
print(len(inventory))  # should be 4 now
```

---

Next mission: `level_1_python_basics/missions/07_monster_dictionary/README.md`
