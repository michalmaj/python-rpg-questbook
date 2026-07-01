# Level 3: Validation and Persistence

**Prerequisite:** Level 2 complete

You have a working, well-structured RPG from Level 2. But there is a problem nobody warned you about: **external data is untrusted**.

The game loads monsters from a JSON file. It saves the hero to disk. It logs combat to CSV. None of this is validated. A single wrong value — a negative HP, a missing field, a changed save format — can crash the game silently or produce wrong results.

Level 3 fixes this. You will learn how to validate data at system boundaries, separate persistence from game logic, and make it easy to swap one storage backend for another.

## The central lesson

```
external data (JSON / CSV / env)
        ↓
Pydantic validation model     ← validates types, constraints, schema version
        ↓
domain dataclass / object     ← game logic lives here, no Pydantic
        ↓
game logic
```

Pydantic validates **at the boundary**. Inside the domain, the Hero and Monster classes from Level 2 remain unchanged.

## Missions

| # | Mission | Concept |
|---|---------|---------|
| 01 | [External Data Is Untrusted](missions/01_external_data_is_untrusted/README.md) | Why raw `json.load()` is dangerous |
| 02 | [Pydantic Monster Config](missions/02_pydantic_monster_config/README.md) | `BaseModel`, `Field`, `ValidationError` |
| 03 | [Load Game Catalogs](missions/03_load_game_catalogs/README.md) | `to_domain()` — Pydantic model → domain dataclass |
| 04 | [Save and Load Game JSON](missions/04_save_and_load_game_json/README.md) | `SaveGameModel`, `schema_version`, round-trip JSON |
| 05 | [Repository Pattern](missions/05_repository_pattern/README.md) | `Protocol`, `JsonSaveRepository`, `InMemorySaveRepository` |
| 06 | [Combat Log Repository](missions/06_combat_log_repository/README.md) | `Literal`, `CsvCombatLogRepository`, validated log rows |
| 07 | [Settings and Paths](missions/07_settings_and_paths/README.md) | `pydantic-settings`, `env_prefix`, `get_settings()` |

**Boss Fight:** [SQLite Repository Backend](projects/01_sqlite_repository_backend/README.md) — add SQLite as a second backend; the game doesn't change.

## Track your progress

```bash
uv run python tools/course_status.py
```
