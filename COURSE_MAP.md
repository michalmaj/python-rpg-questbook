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

**Boss Fight:** *(coming after World 2)*

### World 2: Design

| # | Mission | Concept |
|---|---------|---------|
| 04 | [Type Hints](level_2_oop_and_design/missions/04_type_hints/README.md) | annotations, `->`, mypy |
| 05 | [Enums](level_2_oop_and_design/missions/05_enums/README.md) | `Enum`, replacing magic strings |
| 06 | [Properties](level_2_oop_and_design/missions/06_properties/README.md) | `@property`, computed attributes |
| 07 | [Dataclasses](level_2_oop_and_design/missions/07_dataclasses/README.md) | `@dataclass`, generated `__init__` |

### World 3: Structure

| # | Mission | Concept |
|---|---------|---------|
| 08 | [Module Split](level_2_oop_and_design/missions/08_module_split/README.md) | packages, `__init__.py`, single responsibility |
| 09 | [Pure Functions](level_2_oop_and_design/missions/09_pure_functions/README.md) | side effects, testable logic |
| 10 | [Add Tests](level_2_oop_and_design/missions/10_add_tests/README.md) | pytest, test discovery, assertions |

**Boss Fight:** [Project 01: Refactored RPG](level_2_oop_and_design/projects/01_refactored_rpg/README.md)

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

### World 2: Persistence

| # | Mission | Concept |
|---|---------|---------|
| 04 | [Save and Load Game JSON](level_3_validation_and_persistence/missions/04_save_and_load_game_json/README.md) | `SaveGameModel`, `schema_version`, round-trip JSON |
| 05 | [Repository Pattern](level_3_validation_and_persistence/missions/05_repository_pattern/README.md) | `Protocol`, `JsonSaveRepository`, `InMemorySaveRepository` |

### World 3: Integration

| # | Mission | Concept |
|---|---------|---------|
| 06 | [Combat Log Repository](level_3_validation_and_persistence/missions/06_combat_log_repository/README.md) | `Literal`, `CsvCombatLogRepository`, validated log rows |
| 07 | [Settings and Paths](level_3_validation_and_persistence/missions/07_settings_and_paths/README.md) | `pydantic-settings`, `env_prefix`, `get_settings()` |

**Boss Fight:** [Project 01: SQLite Repository Backend](level_3_validation_and_persistence/projects/01_sqlite_repository_backend/README.md)

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

### World 2: Logging and Observability

| # | Mission | Concept |
|---|---------|---------|
| 03 | [stdlib logging](level_4_interfaces/missions/03_stdlib_logging/README.md) | `logging.getLogger()`, levels, `logger.exception()` |
| 04 | [Log Files](level_4_interfaces/missions/04_log_files/README.md) | `FileHandler`, logger hierarchy, `RotatingFileHandler` |

### World 3: User-Facing Output

| # | Mission | Concept |
|---|---------|---------|
| 05 | [Rich Terminal Output](level_4_interfaces/missions/05_rich_terminal_output/README.md) | `Console`, `Table`, `Panel`, `stderr=True` |
| 06 | [Session Reports](level_4_interfaces/missions/06_session_reports/README.md) | Pydantic report model, `model_dump_json()`, Markdown output |

**Boss Fight:** [Project 01: Installable CLI Tool](level_4_interfaces/projects/01_installable_cli_tool/README.md)
