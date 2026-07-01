# Mission 06: Properties

## Goal

Add `@property` methods that compute values from existing attributes instead of storing them separately.

## You will learn

- The `@property` decorator
- Computed attributes (read-only derived values)
- The difference between an attribute and a property
- When `@property` is more readable than a method

## Game problem

The legacy RPG checks `hero_hp > 0` in multiple places:

```python
while hero_hp > 0 and monster["hp"] > 0:
    ...
if hero_hp <= 0:
    print("You have fallen!")
```

A property lets you write `hero.is_alive` instead — shorter, more readable, and consistent everywhere:

```python
while hero.is_alive and monster.is_alive:
    ...
if not hero.is_alive:
    print("You have fallen!")
```

## Python concept

A **property** is a method that looks like an attribute. The `@property` decorator makes it so callers write `obj.name` instead of `obj.name()`.

```python
class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    @property
    def area(self) -> float:
        return 3.14159 * self.radius ** 2

c = Circle(5)
print(c.area)    # 78.53... — called like an attribute, no ()
c.area = 10      # AttributeError — read-only by default
```

Properties are read-only by default. You do not call them with `()`.

## Your task

Open `task.py`. The `Character` class has `hp` and `max_hp`. Add three properties:

- `is_alive` — returns `True` if `hp > 0`
- `hp_percent` — returns current HP as a percentage of max HP (float 0.0–100.0)
- `status` — returns `"healthy"` if `hp_percent >= 50`, `"wounded"` if `>= 20`, `"critical"` otherwise

## Run

```bash
uv run python level_2_oop_and_design/missions/06_properties/task.py
```

## Check

```bash
uv run python level_2_oop_and_design/missions/06_properties/check.py
```

## Break it on purpose

Try assigning to a property: `hero.is_alive = False`. What error do you get?

## Fix it

Properties are read-only by default. If you need a settable property, you add a `@name.setter` — but for derived values like `is_alive` that is almost never the right choice.

## Side quest

Add a `@property` called `summary` that returns a one-line string like:
```
Ada (warrior) — HP: 85/120 [71%] — HEALTHY
```

## Real-world translation

Django model fields use properties for computed values: `user.full_name`, `order.total_price`, `article.is_published`. Pandas uses them for `df.shape`, `df.dtypes`, `df.empty`. Properties are everywhere.

## Checklist

- [ ] I can add `@property` to a method
- [ ] I know that properties are accessed without `()` — `obj.prop`, not `obj.prop()`
- [ ] I can compute a value from other attributes inside a property
- [ ] I understand that properties are read-only by default
- [ ] I can use one property inside another property

---

Next mission: `level_2_oop_and_design/missions/07_dataclasses/README.md`
