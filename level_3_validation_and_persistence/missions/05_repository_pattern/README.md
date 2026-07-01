# Mission 05: Repository Pattern

## Goal

Wrap save and load behind a `Protocol` so the game code never knows whether it is talking to a JSON file, a SQLite database, or an in-memory dict (useful for tests).

## You will learn

- `typing.Protocol` as a lightweight interface definition
- Why game code should depend on an abstraction, not a concrete class
- `InMemorySaveRepository` as a test double
- How swapping backends (JSON → SQLite) becomes a one-line change in game code

## Game problem

The starter game calls `save_game(hero)` and `load_game()` directly. Both functions are hard-coded to use JSON files. If you want to:

- Switch to SQLite storage
- Run tests without writing to disk
- Support multiple save slots

...you must modify the game loop itself. That is a violation of separation of concerns: the game loop should not know how saving works.

The repository pattern wraps persistence behind an interface:

```python
class SaveRepository(Protocol):
    def save(self, hero: Hero) -> None: ...
    def load(self) -> Hero | None: ...
```

The game loop now looks like:

```python
def run_game(repo: SaveRepository) -> None:
    hero = repo.load() or choose_hero()
    ...
    repo.save(hero)
```

It doesn't care whether `repo` is a `JsonSaveRepository` or a `SqliteSaveRepository`.

## Python concept

**`Protocol`** defines a structural interface — no inheritance required. Any class that has the right methods satisfies the protocol automatically.

```python
from typing import Protocol

class SaveRepository(Protocol):
    def save(self, hero: Hero) -> None: ...
    def load(self) -> Hero | None: ...

class JsonSaveRepository:          # does NOT inherit SaveRepository
    def save(self, hero: Hero) -> None:
        ...
    def load(self) -> Hero | None:
        ...

repo: SaveRepository = JsonSaveRepository()   # ✅ type checker is happy
```

**`InMemorySaveRepository`** stores data in a variable. It is useful in tests because it never touches the filesystem:

```python
class InMemorySaveRepository:
    def __init__(self) -> None:
        self._data: Hero | None = None

    def save(self, hero: Hero) -> None:
        self._data = hero

    def load(self) -> Hero | None:
        return self._data
```

## Your task

Open `task.py`. `SaveGameModel` and both domain classes are already provided.

Implement:

1. **`JsonSaveRepository.save(hero)`** — create a `SaveGameModel`, write to `self.path`
2. **`JsonSaveRepository.load()`** — return `None` if no file; parse, validate schema version, return hero
3. **`InMemorySaveRepository.save(hero)`** — store in `self._data`
4. **`InMemorySaveRepository.load()`** — return `self._data`

## Run

> Before you complete the TODOs, running `task.py` will print a friendly reminder instead of crashing.

```bash
uv run python level_3_validation_and_persistence/missions/05_repository_pattern/task.py
```

## Check

```bash
uv run python level_3_validation_and_persistence/missions/05_repository_pattern/check.py
```

## Break it on purpose

Change `run_game_session(repo)` to use `JsonSaveRepository()` directly instead of the `repo` argument. Now try passing an `InMemorySaveRepository`. The function ignores it — the abstraction is broken.

## Fix it

Pass `repo` to the function and let the function call `repo.save()` / `repo.load()`. The function never references the concrete class.

## Side quest

Write a test using `InMemorySaveRepository`:

```python
def test_gold_persists_between_sessions() -> None:
    repo = InMemorySaveRepository()
    run_game_session(repo)
    hero = repo.load()
    assert hero is not None
    assert hero.gold == 10    # or whatever run_game_session adds
```

## Real-world translation

The Repository pattern comes from Domain-Driven Design. Django's ORM, SQLAlchemy, and FastAPI's dependency injection all use variations of it. The key insight: business logic should depend on an abstraction over storage, not on a specific storage engine.

## Checklist

- [ ] `JsonSaveRepository.save()` and `.load()` work with a real file
- [ ] `InMemorySaveRepository.save()` and `.load()` work without touching disk
- [ ] I understand that `Protocol` defines an interface without inheritance
- [ ] I know why `InMemorySaveRepository` is useful in tests
- [ ] I can explain: what does the game loop gain by depending on `SaveRepository` instead of `JsonSaveRepository`?

---

Next mission: `level_3_validation_and_persistence/missions/06_combat_log_repository/README.md`
