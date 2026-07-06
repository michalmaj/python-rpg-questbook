# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versions are tagged on `main` after each milestone.

---

## [1.0.0] — 2026-07-06

First stable release. All seven levels are complete, including two checkpoint projects and one boss fight per level.

### Added — Release infrastructure
- GitHub Actions CI (`ci.yml`): runs `author_check.py`, `ruff check tools/`, and `uv run rpg --help` on every push and PR
- CI badge and Python badge in `README.md`
- `CHANGELOG.md` (this file)
- GitHub PR template with type checkboxes and author-check reminder
- GitHub issue templates: Bug Report, Content Issue, Feature Request, New Mission/Project Proposal

### Added — Level 7 checkpoint projects (PR #47)
- `P01 Async Quest Aggregator` — `asyncio.gather` with per-source timeout (`asyncio.wait_for`)
- `P02 Background Report Queue` — daemon thread worker with `InMemoryJobRepository`, FastAPI integration

### Fixed — Stabilization sprint (PR #48)
- `L7/P01`: closed timing false-positive by monkey-patching `SOURCES` with controlled coroutines
- `L7/P02`: added behavioural `threading.Event` test for `BackgroundWorker` (gate 11)
- `L6/P01`: replaced `HTTPException` with `Literal["goblin","orc","dragon"]` so Pydantic auto-422s invalid names
- `L6/P02`: repository layer now returns domain `Monster` dataclasses, not `MonsterOut` schemas
- `L5/P01`: removed `pyproject.toml` that broke uv workspace; split into `ruff.toml`, `mypy.ini`, `pyrightconfig.json`
- `L5/P02`: added `strict=True` to xfail gate, relaxed quota counts, coverage failure now raises `SystemExit(1)`
- `L4/P02`: added `@app.callback()` so Typer enables multi-command mode
- `L3/P01`: `name: str` → `name: str = Field(..., min_length=1)` in `MonsterModel`; gate count updated
- `L2/P01`: `is_alive` changed from `@property` to plain method
- `pyproject.toml`: corrected `packages` path `01_installable_cli_tool` → `03_installable_cli_tool`
- `tools/author_check.py`: smoke-tests `uv run rpg --help`; README-link checker covers L7

---

## [0.7.0] — Level 7: Concurrency and Background Work

### Added (PR #40, #41)
- 8 missions: blocking vs background, asyncio basics, async API endpoints, job-status repository, background jobs, `ThreadPoolExecutor`, `ProcessPoolExecutor`, testing background work
- Starter: blocking tournament API (`starter_blocking_rpg_api/`)
- Boss fight (`P03`): concurrent tournament runner — FastAPI + `ProcessPoolExecutor`, full test suite

### Fixed (PR #41 — stabilization)
- `M02`: corrected concurrency vs parallelism language
- `M03`: rewrote `async def` messaging to be pedagogically accurate
- `M06`: removed unused `import time`; AST-checks `ThreadPoolExecutor` usage inside function body
- `M07`: AST-checks `ProcessPoolExecutor` usage inside function body; guard comment
- `M05`: `SyncWorker` via `dependency_overrides` in API check
- Boss fight: restored scaffold in `tournaments.py` and `test_api.py`; require ≥6 test functions via AST
- `tools/`: L7 wired into `author_check.py`, `course_status.py`, `COURSE_MAP.md`

---

## [0.6.0] — Level 6: API with FastAPI

### Added (PR #38)
- 8 missions: FastAPI intro, path parameters, request bodies, schemas, routers, dependency injection, error handling, TestClient
- Starter: service-ready RPG engine (`starter_service_ready_rpg/`)
- Boss fight (`P03`): RPG Battle API — 7 endpoints, JSON persistence, `HeroClass` enum, `SessionCreated` schema

### Fixed (PR #39 — stabilization)
- Renamed `def_` → `defense` in `MonsterOut` for a clean HTTP API surface
- `hero_class: str` → `HeroClass` enum for proper 422 validation; Gate 5b added
- Removed local `pyproject.toml` / `uv.lock` that broke uv workspace resolution
- Gate 8 content-type check; `BattleRequest.hero_class` in schemas; M02 README import path
- L6 README: clarified run paths (repo root vs mission folder)

### Added (PR #46 — checkpoint projects)
- `P01 Battle Preview API` — Pydantic `Literal` type for monster validation, TestClient gates
- `P02 Monster Catalog API` — `Monster` domain dataclass, `MonsterRepository` Protocol, full API gates

---

## [0.5.0] — Level 5: Maintainability

### Added (PR #36)
- 9 missions: ruff, mypy, pyright, pytest fixtures, `parametrize`, coverage, error handling, pre-commit, GitHub Actions CI
- Starter: working RPG with 6 quality smells (`starter_unqualified_rpg/`)
- Boss fight (`P03`): full release pipeline — ruff + mypy + coverage gate

### Fixed (PR #37 — L4 boss functional checks)
- L4 boss fight checker: fixed false-positive where `NotImplementedError` silently passed gates

### Added (PR #45 — checkpoint projects)
- `P01 Quality Gate Rescue` — standalone ruff/mypy/coverage configs; buggy starter to fix
- `P02 Combat Regression Suite` — `xfail(strict=True)` bug regression pattern, ≥85% coverage gate

---

## [0.4.0] — Level 4: Interfaces

### Added (PR #34)
- 6 missions: Typer CLI, `argparse`, stdlib logging, Rich output, JSON + Markdown reports, installable entry point
- Starter: verbose RPG with interface smells (`starter_verbose_rpg/`)
- Boss fight (`P03`): installable CLI tool (`uv run rpg`)

### Fixed (PR #35 — stabilization)
- Various gate and scaffold fixes following first run-through

### Added (PR #44 — checkpoint projects)
- `P01 Quest Master CLI` — multi-command Typer CLI with `@app.callback()`
- `P02 Observable Battle Runner` — logging + Rich progress integrated into battle loop

---

## [0.3.0] — Level 3: Validation and Persistence

### Added (PR #30, #33)
- 7 missions: Pydantic models, field validators, repository pattern, JSON persistence, CSV persistence, SQLite with `sqlite3`, SQLite with SQLAlchemy
- Starter: raw RPG without validation (`starter_raw_rpg/`)
- Boss fight (`P03`): SQLite repository backend

### Fixed (PR #31, #32 — stabilization)
- Gate corrections and scaffold fixes

### Added (PR #43 — checkpoint projects)
- `P01 Validated Bestiary` — Pydantic `MonsterModel` with field constraints, batch validation gates
- `P02 Save Slot Manager` — JSON save/load, slot management, repository pattern

---

## [0.2.0] — Level 2: OOP and Design

### Added (PR #28)
- 10 missions: classes, `__init__`, methods, inheritance, `super()`, `dataclasses`, `__str__` / `__repr__`, `@staticmethod`, `@classmethod`, refactoring and testing
- Starter: legacy procedural RPG (`starter_legacy_rpg/`)
- Boss fight (`P03`): refactored RPG with full OOP design

### Fixed (PR #29 — stabilization)
- Gate corrections, README paths, check.py assertion fixes

### Added (PR #42 — checkpoint projects)
- `P01 Arena Roster` — `Hero` / `Monster` classes, `is_alive()`, arena management
- `P02 Character Sheet Builder` — dataclasses, `__str__`, optional fields

---

## [0.1.0] — Level 1: Python Basics

### Added (PR #1)
- Course architecture: `uv` workspace, `pyproject.toml`, `tools/`, `COURSE_MAP.md`

### Added (PR #2)
- Concept progression refactor — all L1 missions ordered and scaffolded

### Added (PR #3 – #15) — Missions 04–15
- M04 `combat_loop` — `while` loop as combat turns
- M05 `for_loop` — iterating over enemy lists
- M06 `lists` — enemy roster management
- M07 `dicts` — character sheets as dictionaries
- M08 `functions` — `attack()`, `heal()`, `roll_damage()`
- M09 `random` — dice rolls and loot drops
- M10 `exceptions` — handling invalid moves and game-over states
- M11 `files` — writing and reading combat logs
- M12 `json` — saving game state as JSON
- M13 `modules` — splitting the game into files
- M14 `dataclass` — hero and monster as dataclasses
- M15 `pytest` — writing first tests for game logic

### Added (PR #16 – #22) — Projects and data analysis
- Project 04: Full RPG — the complete terminal game combining all L1 concepts
- M16 `numpy` — analyzing combat log arrays
- M17 `numpy_stats` — damage distributions and balance checks
- M18 `pandas` — loading and querying combat logs as DataFrames
- M19 `groupby` — comparing hero classes and enemy difficulty
- M20 `matplotlib` — plotting combat data
- Project 05: Analytics — end-to-end analysis of generated combat logs

### Fixed (PR #23 — review stabilization)
- Gate corrections and README polish following first review

### Added (PR #24)
- Project 02: Turn-based combat — the first full boss fight of Level 1

### Fixed (PR #25, #26, #27)
- Course polish, pre-pilot sprint fixes, L1 reorganization

---

[1.0.0]: https://github.com/michalmaj/python-rpg-questbook/releases/tag/v1.0.0
