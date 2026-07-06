# Course Map

> This file is your GPS — read it, but do not edit it.
> Track your progress: `uv run python tools/course_status.py`

---

## Part 1: Python Core

### World 1: First Hero

| # | Mission | Concept |
|---|---------|---------|
| 01 | [Hero Stats](level_1_python_basics/missions/01_hero_stats/README.md) | variables, str, int |
| 02 | [Damage and Healing](level_1_python_basics/missions/02_damage_and_healing/README.md) | arithmetic, min/max |
| 03 | [Choose Your Hero](level_1_python_basics/missions/03_choose_your_hero/README.md) | input, if/elif/else |

**Boss Fight:** [Project 01: Battle Calculator](level_1_python_basics/projects/01_battle_calculator/README.md)

---

### World 2: Combat Logic

| # | Mission | Concept |
|---|---------|---------|
| 04 | [Combat Loop](level_1_python_basics/missions/04_combat_loop/README.md) | while loop |
| 05 | [Arena Challenge](level_1_python_basics/missions/05_arena_challenge/README.md) | for loop, range() |
| 06 | [Hero Inventory](level_1_python_basics/missions/06_hero_inventory/README.md) | lists, append, len |

**Boss Fight:** [Project 02: Turn-Based Combat](level_1_python_basics/projects/02_turn_based_combat/README.md)

---

### World 3: Character Data

| # | Mission | Concept |
|---|---------|---------|
| 07 | [Monster Dictionary](level_1_python_basics/missions/07_monster_dictionary/README.md) | dictionaries |
| 08 | [Attack Function](level_1_python_basics/missions/08_attack_function/README.md) | functions, def, return |
| 09 | [Dice Rolls](level_1_python_basics/missions/09_dice_rolls/README.md) | import, random.randint |
| 10 | [Safe Input](level_1_python_basics/missions/10_safe_input/README.md) | try/except, ValueError |

**Boss Fight:** [Project 03: Terminal RPG](level_1_python_basics/projects/03_terminal_rpg/README.md)

---

### World 4: Saving and Structure

| # | Mission | Concept |
|---|---------|---------|
| 11 | [Combat Log](level_1_python_basics/missions/11_combat_log/README.md) | open, write, CSV |
| 12 | [Save Game](level_1_python_basics/missions/12_save_game/README.md) | json.dump, json.load |
| 13 | [Split the Game](level_1_python_basics/missions/13_split_the_game/README.md) | modules, from X import Y |
| 14 | [Hero Dataclass](level_1_python_basics/missions/14_hero_dataclass/README.md) | dataclasses, type annotations |
| 15 | [Test the Damage](level_1_python_basics/missions/15_test_the_damage/README.md) | pytest, assert |

**Boss Fight:** [Project 04: Full Terminal RPG](level_1_python_basics/projects/04_full_rpg/README.md)

---

## Part 2: Game Data Analysis

After you build the RPG, you will analyze the game data.

| # | Mission | Concept |
|---|---------|---------|
| 16 | [Dice Are Data](level_1_python_basics/missions/16_dice_are_data/README.md) | NumPy arrays, np.random.randint |
| 17 | [Damage Distributions](level_1_python_basics/missions/17_damage_distributions/README.md) | std, percentile |
| 18 | [Read Combat Logs](level_1_python_basics/missions/18_read_combat_logs/README.md) | pd.read_csv, DataFrame |
| 19 | [Filter and Group](level_1_python_basics/missions/19_filter_and_group/README.md) | groupby, filter, sort_values |
| 20 | [Plot the Results](level_1_python_basics/missions/20_plot_the_results/README.md) | plt.plot, plt.bar, savefig |

**Final Boss:** [Project 05: Game Analytics Report](level_1_python_basics/projects/05_analytics_report/README.md)

---

*Is the game balanced? You will find out.*

---

## Level 2: OOP and Design

**Prerequisite:** Level 1 complete

You inherited messy code. Now you fix it.

### World 1: Objects

| # | Mission | Concept |
|---|---------|---------|
| 01 | [Extract Hero](level_2_oop_and_design/missions/01_extract_hero/README.md) | classes, `__init__`, instance attributes |
| 02 | [Monster Class](level_2_oop_and_design/missions/02_monster_class/README.md) | methods, `self`, behaviour on objects |
| 03 | [Character Base](level_2_oop_and_design/missions/03_character_base/README.md) | inheritance, `super().__init__()` |

**Checkpoint:** [Project 01: Arena Roster](level_2_oop_and_design/projects/01_arena_roster/README.md)

### World 2: Design

| # | Mission | Concept |
|---|---------|---------|
| 04 | [Type Hints](level_2_oop_and_design/missions/04_type_hints/README.md) | annotations, `->`, mypy |
| 05 | [Enums](level_2_oop_and_design/missions/05_enums/README.md) | `Enum`, replacing magic strings |
| 06 | [Properties](level_2_oop_and_design/missions/06_properties/README.md) | `@property`, computed attributes |
| 07 | [Dataclasses](level_2_oop_and_design/missions/07_dataclasses/README.md) | `@dataclass`, generated `__init__` |

**Checkpoint:** [Project 02: Character Sheet Builder](level_2_oop_and_design/projects/02_character_sheet_builder/README.md)

### World 3: Structure

| # | Mission | Concept |
|---|---------|---------|
| 08 | [Module Split](level_2_oop_and_design/missions/08_module_split/README.md) | packages, `__init__.py`, single responsibility |
| 09 | [Pure Functions](level_2_oop_and_design/missions/09_pure_functions/README.md) | side effects, testable logic |
| 10 | [Add Tests](level_2_oop_and_design/missions/10_add_tests/README.md) | pytest, test discovery, assertions |

**Boss Fight:** [Project 03: Refactored RPG](level_2_oop_and_design/projects/03_refactored_rpg/README.md)

---

## Level 3: Validation and Persistence

**Prerequisite:** Level 2 complete

External data is untrusted. Validate at boundaries, isolate persistence from domain logic.

### World 1: Trusted Data

| # | Mission | Concept |
|---|---------|---------|
| 01 | [External Data Is Untrusted](level_3_validation_and_persistence/missions/01_external_data_is_untrusted/README.md) | why raw `json.load()` is dangerous |
| 02 | [Pydantic Monster Config](level_3_validation_and_persistence/missions/02_pydantic_monster_config/README.md) | `BaseModel`, `Field`, `ValidationError` |
| 03 | [Load Game Catalogs](level_3_validation_and_persistence/missions/03_load_game_catalogs/README.md) | `to_domain()` — Pydantic model → domain dataclass |

**Checkpoint:** [Project 01: Validated Bestiary](level_3_validation_and_persistence/projects/01_validated_bestiary/README.md)

### World 2: Persistence

| # | Mission | Concept |
|---|---------|---------|
| 04 | [Save and Load Game JSON](level_3_validation_and_persistence/missions/04_save_and_load_game_json/README.md) | `SaveGameModel`, `schema_version`, round-trip JSON |
| 05 | [Repository Pattern](level_3_validation_and_persistence/missions/05_repository_pattern/README.md) | `Protocol`, `JsonSaveRepository`, `InMemorySaveRepository` |

**Checkpoint:** [Project 02: Save Slot Manager](level_3_validation_and_persistence/projects/02_save_slot_manager/README.md)

### World 3: Integration

| # | Mission | Concept |
|---|---------|---------|
| 06 | [Combat Log Repository](level_3_validation_and_persistence/missions/06_combat_log_repository/README.md) | `Literal`, `CsvCombatLogRepository`, validated log rows |
| 07 | [Settings and Paths](level_3_validation_and_persistence/missions/07_settings_and_paths/README.md) | `pydantic-settings`, `env_prefix`, `get_settings()` |

**Boss Fight:** [Project 03: SQLite Repository Backend](level_3_validation_and_persistence/projects/03_sqlite_repository_backend/README.md)

---

## Level 4: Interfaces and Reports

**Prerequisite:** Level 3 complete

The game has domain logic, validation, and persistence.
Now it needs a real interface: CLI commands, logging, readable terminal output, and reports.

### World 1: Command Line Interface

| # | Mission | Concept |
|---|---------|---------|
| 01 | [argparse Baseline](level_4_interfaces/missions/01_argparse_baseline/README.md) | `argparse`, subcommands, `add_subparsers`, `choices=` |
| 02 | [Typer CLI](level_4_interfaces/missions/02_typer_cli/README.md) | `typer.Typer()`, `@app.command()`, type hints as CLI contract |

**Checkpoint:** [Project 01: Quest Master CLI](level_4_interfaces/projects/01_quest_master_cli/README.md)

### World 2: Logging and Observability

| # | Mission | Concept |
|---|---------|---------|
| 03 | [stdlib logging](level_4_interfaces/missions/03_stdlib_logging/README.md) | `logging.getLogger()`, levels, `logger.exception()` |
| 04 | [Log Files](level_4_interfaces/missions/04_log_files/README.md) | `FileHandler`, logger hierarchy, `RotatingFileHandler` |

**Checkpoint:** [Project 02: Observable Battle Runner](level_4_interfaces/projects/02_observable_battle_runner/README.md)

### World 3: User-Facing Output

| # | Mission | Concept |
|---|---------|---------|
| 05 | [Rich Terminal Output](level_4_interfaces/missions/05_rich_terminal_output/README.md) | `Console`, `Table`, `Panel`, `stderr=True` |
| 06 | [Session Reports](level_4_interfaces/missions/06_session_reports/README.md) | Pydantic report model, `model_dump_json()`, Markdown output |

**Boss Fight:** [Project 03: Installable CLI Tool](level_4_interfaces/projects/03_installable_cli_tool/README.md)

---

## Level 5: Production Quality and Maintainability

> **Prerequisite:** Level 4 complete (installable CLI with Typer, Rich, logging, session reports).

**Central thesis:** Your tool works. Now can a new developer understand it, change it safely, and ship it with confidence?

### World 1: Static Analysis

| Mission | Concept | Key tool |
|---------|---------|----------|
| [M01: ruff Linting](level_5_maintainability/missions/01_ruff_linting/README.md) | Lint + style | ruff |
| [M02: mypy Type Checking](level_5_maintainability/missions/02_mypy_type_checking/README.md) | Static types | mypy --strict |
| [M03: pyright Strict](level_5_maintainability/missions/03_pyright_strict/README.md) | Second type checker | pyright --strict |

**Checkpoint:** [Project 01: Quality Gate Rescue](level_5_maintainability/projects/01_quality_gate_rescue/README.md)

### World 2: Testing

| Mission | Concept | Key tool |
|---------|---------|----------|
| [M04: pytest Fixtures](level_5_maintainability/missions/04_pytest_fixtures/README.md) | Test setup | @pytest.fixture |
| [M05: pytest Parametrize](level_5_maintainability/missions/05_pytest_parametrize/README.md) | Edge cases | @pytest.mark.parametrize |
| [M06: Coverage](level_5_maintainability/missions/06_coverage/README.md) | Test coverage | pytest-cov |

**Checkpoint:** [Project 02: Combat Regression Suite](level_5_maintainability/projects/02_combat_regression_suite/README.md)

### World 3: CI/CD and Polish

| Mission | Concept | Key tool |
|---------|---------|----------|
| [M07: Error Handling](level_5_maintainability/missions/07_error_handling/README.md) | Exception hierarchy | RPGError |
| [M08: pre-commit](level_5_maintainability/missions/08_pre_commit/README.md) | Local quality gate | pre-commit |
| [M09: GitHub Actions CI](level_5_maintainability/missions/09_github_actions_ci/README.md) | Remote CI | GitHub Actions |

**Boss Fight:** [Project 03: Full Release Pipeline](level_5_maintainability/projects/03_full_release_pipeline/README.md) — wire all 9 tools, write CHANGELOG, tag v1.0.0.

---

## Level 6: API Interface with FastAPI

> **Prerequisite:** Level 5 complete (production-quality CLI with tests and CI).

**Central thesis:** The RPG engine works — now expose it to the world. FastAPI turns Python functions into documented, type-safe HTTP endpoints in minutes.

### World 1: HTTP Basics

| Mission | Concept | Key tool |
|---------|---------|----------|
| [M01: First FastAPI App](level_6_api/missions/01_first_fastapi_app/README.md) | App setup, /docs | FastAPI, uvicorn |
| [M02: Request/Response Schemas](level_6_api/missions/02_request_response_schemas/README.md) | Pydantic schemas for HTTP | BaseModel |
| [M03: Routes Call Services](level_6_api/missions/03_routes_call_services/README.md) | Thin routes, no logic | service layer |

**Checkpoint:** [Project 01: Battle Preview API](level_6_api/projects/01_battle_preview_api/README.md)

### World 2: Structure and DI

| Mission | Concept | Key tool |
|---------|---------|----------|
| [M04: API Routers](level_6_api/missions/04_api_routers/README.md) | File split | APIRouter |
| [M05: Dependencies and Repositories](level_6_api/missions/05_dependencies_and_repositories/README.md) | DI factories | Depends() |
| [M06: API Errors and Status Codes](level_6_api/missions/06_api_errors_and_status_codes/README.md) | Error handling | HTTPException |

**Checkpoint:** [Project 02: Monster Catalog API](level_6_api/projects/02_monster_catalog_api/README.md)

### World 3: Quality and Polish

| Mission | Concept | Key tool |
|---------|---------|----------|
| [M07: API Tests](level_6_api/missions/07_api_tests/README.md) | HTTP-level tests | TestClient |
| [M08: OpenAPI and API Polish](level_6_api/missions/08_openapi_and_api_polish/README.md) | Docs polish | tags, descriptions |

**Boss Fight:** [Project 03: RPG Battle API](level_6_api/projects/03_rpg_battle_api/README.md) — wire all 8 concepts into a fully tested 7-endpoint battle API with JSON session persistence.

---

## Level 7: Concurrency and Background Work

> **Prerequisite:** Level 6 complete (FastAPI API with tests).

**Central thesis:** The API works — but long operations block it. Learn to return a `job_id` immediately and execute work in the background.

| # | Mission | Skill |
|---|---------|-------|
| 01 | [Blocking vs Background Work](level_7_concurrency_and_background_work/missions/01_blocking_vs_background_work/README.md) | See the blocking problem |
| 02 | [asyncio Basics](level_7_concurrency_and_background_work/missions/02_asyncio_basics/README.md) | async/await, gather, wait_for |
| 03 | [Async API Endpoints](level_7_concurrency_and_background_work/missions/03_async_api_endpoints/README.md) | async def in FastAPI; I/O vs CPU |
| 04 | [Background Jobs](level_7_concurrency_and_background_work/missions/04_background_jobs/README.md) | job_id pattern, threading.Thread |
| 05 | [Job Status Repository](level_7_concurrency_and_background_work/missions/05_job_status_repository/README.md) | JobRepository Protocol |
| 06 | [Thread Pool for Blocking I/O](level_7_concurrency_and_background_work/missions/06_thread_pool_for_blocking_io/README.md) | ThreadPoolExecutor |
| 07 | [Process Pool for CPU Work](level_7_concurrency_and_background_work/missions/07_process_pool_for_cpu_work/README.md) | ProcessPoolExecutor |
| 08 | [Testing Background Work](level_7_concurrency_and_background_work/missions/08_testing_background_work/README.md) | SyncWorker, deterministic tests |

**Boss Fight:** [Concurrent Tournament Runner](level_7_concurrency_and_background_work/projects/01_concurrent_tournament_runner/README.md)
