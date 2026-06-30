# Mission 06: Hero Inventory

## Goal

Give the hero a bag that can hold multiple items.

## You will learn

- Lists — ordered collections of values
- `append()` — add an item to the end of a list
- `len()` — count how many items are in a list
- `for item in list` — loop directly over a list's contents

## Game problem

The hero picks up items during the adventure: weapons, potions, scrolls.
We need a way to store them all and loop over them — that's what a list is for.

## Your task

Open `task.py`. The hero already has two starting items.
Add three more and display the full inventory.

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
```

## Check

```bash
uv run python missions/06_hero_inventory/check.py
```

## Side quest

After building the inventory, explore indexing:

```python
print(inventory[0])    # first item
print(inventory[-1])   # last item — negative index counts from the end
```

Try removing an item:
```python
inventory.remove("gold coin")
print(len(inventory))  # should be 4 now
```

---

Next mission: `missions/07_monster_dictionary/README.md`
