"""check.py — Boss Fight: SQLite Repository Backend"""

import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).parents[3]
PROGRESS_FILE = REPO_ROOT / "level_3_validation_and_persistence" / ".progress"


def update_progress(project_id: str) -> None:
    progress: dict = {"missions": {}, "projects": {}}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    progress["projects"][project_id] = "complete"
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


def main() -> None:
    import importlib.util

    project_dir = Path(__file__).parent

    # Add project dir to sys.path so "from rpg.domain import ..." works
    sys.path.insert(0, str(project_dir))

    # Import submodules
    def load(rel: str):  # noqa: ANN202
        path = project_dir / rel
        spec = importlib.util.spec_from_file_location(rel.replace("/", ".").removesuffix(".py"), path)
        mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        return mod

    try:
        save_mod = load("rpg/save_repo.py")
        log_mod = load("rpg/log_repo.py")
        domain_mod = load("rpg/domain.py")
        schemas_mod = load("rpg/schemas.py")
    except Exception as e:
        print(f"❌ Could not import project modules: {e}")
        raise SystemExit(1)

    # domain.py must be free of Pydantic
    domain_src = (project_dir / "rpg" / "domain.py").read_text()
    if "BaseModel" in domain_src or "from pydantic" in domain_src:
        print("❌ rpg/domain.py imports Pydantic — domain must be pure dataclasses/enums only.")
        raise SystemExit(1)

    SqliteSaveRepository = getattr(save_mod, "SqliteSaveRepository", None)
    JsonSaveRepository = getattr(save_mod, "JsonSaveRepository", None)
    SqliteCombatLogRepository = getattr(log_mod, "SqliteCombatLogRepository", None)
    CsvCombatLogRepository = getattr(log_mod, "CsvCombatLogRepository", None)
    Hero = getattr(domain_mod, "Hero", None)
    HeroClass = getattr(domain_mod, "HeroClass", None)
    CombatLogRow = getattr(schemas_mod, "CombatLogRow", None)

    for name, obj in [("SqliteSaveRepository", SqliteSaveRepository),
                      ("JsonSaveRepository", JsonSaveRepository),
                      ("SqliteCombatLogRepository", SqliteCombatLogRepository),
                      ("CsvCombatLogRepository", CsvCombatLogRepository),
                      ("Hero", Hero), ("HeroClass", HeroClass), ("CombatLogRow", CombatLogRow)]:
        if obj is None:
            print(f"❌ {name} not found.")
            raise SystemExit(1)

    hero = Hero(
        name="Turing", hero_class=HeroClass.MAGE,
        hp=80, max_hp=80, atk=18, def_=2,
        potions=3, gold=100, wins=5, losses=0,
    )

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "test.db"

        # --- SqliteSaveRepository ---
        try:
            save_repo = SqliteSaveRepository(db_path)
        except NotImplementedError:
            print("❌ SqliteSaveRepository.__init__() is not implemented yet.")
            raise SystemExit(1)
        except Exception as e:
            print(f"❌ SqliteSaveRepository.__init__() raised: {e}")
            raise SystemExit(1)

        result = save_repo.load()
        if result is not None:
            print("❌ SqliteSaveRepository.load() should return None before any save.")
            raise SystemExit(1)

        try:
            save_repo.save(hero)
        except NotImplementedError:
            print("❌ SqliteSaveRepository.save() is not implemented yet.")
            raise SystemExit(1)

        try:
            loaded = save_repo.load()
        except NotImplementedError:
            print("❌ SqliteSaveRepository.load() is not implemented yet.")
            raise SystemExit(1)

        if loaded is None:
            print("❌ SqliteSaveRepository.load() returned None after saving.")
            raise SystemExit(1)
        if loaded.name != "Turing" or loaded.gold != 100:
            print(f"❌ Loaded hero has wrong data: {loaded}")
            raise SystemExit(1)

        # Schema version mismatch
        import sqlite3
        con = sqlite3.connect(db_path)
        con.execute("UPDATE saves SET schema_ver = 99 WHERE id = 1")
        con.commit()
        con.close()
        try:
            save_repo.load()
            print("❌ SqliteSaveRepository.load() should raise ValueError on schema version mismatch.")
            raise SystemExit(1)
        except ValueError:
            pass
        except NotImplementedError:
            print("❌ Schema version check not implemented in SqliteSaveRepository.load().")
            raise SystemExit(1)

        # --- JsonSaveRepository (ported from Mission 05) ---
        # This backend must satisfy the same SaveRepository contract as the
        # Sqlite one — a boss fight that only proves the *new* backend works
        # isn't proving "the game doesn't know which backend is running".
        json_path = Path(tmp) / "save_game.json"
        try:
            json_repo = JsonSaveRepository(json_path)
        except NotImplementedError:
            print("❌ JsonSaveRepository.__init__() is not implemented yet.")
            raise SystemExit(1)

        try:
            result = json_repo.load()
        except NotImplementedError:
            print("❌ JsonSaveRepository.load() is not implemented yet.")
            raise SystemExit(1)
        if result is not None:
            print("❌ JsonSaveRepository.load() should return None before any save.")
            raise SystemExit(1)

        try:
            json_repo.save(hero)
        except NotImplementedError:
            print("❌ JsonSaveRepository.save() is not implemented yet.")
            raise SystemExit(1)

        try:
            json_loaded = json_repo.load()
        except NotImplementedError:
            print("❌ JsonSaveRepository.load() is not implemented yet.")
            raise SystemExit(1)

        if json_loaded is None:
            print("❌ JsonSaveRepository.load() returned None after saving.")
            raise SystemExit(1)
        # Note: don't compare json_loaded.hero_class to HeroClass.MAGE here —
        # save_repo.py imports HeroClass via the normal package import system
        # while this checker loads rpg/domain.py through a separate
        # importlib spec, so the two HeroClass classes are not `is`-identical
        # even when they represent the same value. .value compares safely.
        if (
            json_loaded.name != "Turing"
            or json_loaded.gold != 100
            or json_loaded.wins != 5
            or json_loaded.hero_class.value != "mage"
        ):
            print(f"❌ JsonSaveRepository round-trip has wrong data: {json_loaded}")
            raise SystemExit(1)

        json_raw = json.loads(json_path.read_text())
        json_raw["schema_version"] = 99
        json_path.write_text(json.dumps(json_raw))
        try:
            json_repo.load()
            print("❌ JsonSaveRepository.load() should raise ValueError on schema version mismatch.")
            raise SystemExit(1)
        except ValueError:
            pass
        except NotImplementedError:
            print("❌ Schema version check not implemented in JsonSaveRepository.load().")
            raise SystemExit(1)

        # --- SqliteCombatLogRepository ---
        log_db = Path(tmp) / "log.db"
        try:
            log_repo = SqliteCombatLogRepository(log_db)
        except NotImplementedError:
            print("❌ SqliteCombatLogRepository.__init__() is not implemented yet.")
            raise SystemExit(1)

        empty = log_repo.read_all()
        if empty != []:
            print(f"❌ read_all() before any append should return [], got {empty}")
            raise SystemExit(1)

        row = CombatLogRow(
            battle_id=1, turn=1,
            hero_name="Turing", hero_class="mage", monster="Dragon",
            action="attack", damage_dealt=20, damage_taken=15,
            hero_hp=65, monster_hp=100, result="ongoing",
        )
        try:
            log_repo.append(row)
        except NotImplementedError:
            print("❌ SqliteCombatLogRepository.append() is not implemented yet.")
            raise SystemExit(1)

        row2 = CombatLogRow(
            battle_id=1, turn=2,
            hero_name="Turing", hero_class="mage", monster="Dragon",
            action="attack", damage_dealt=25, damage_taken=0,
            hero_hp=65, monster_hp=0, result="win",
        )
        log_repo.append(row2)

        rows = log_repo.read_all()
        if len(rows) != 2:
            print(f"❌ Expected 2 rows, got {len(rows)}")
            raise SystemExit(1)
        # Note: not isinstance(rows[0], CombatLogRow) — rpg/log_repo.py imports
        # CombatLogRow via the normal package import system while this checker
        # loads rpg/schemas.py through a separate importlib spec, so the two
        # CombatLogRow classes are not `is`-identical even for a fully correct
        # solution. Comparing the class name is identity-agnostic.
        if type(rows[0]).__name__ != "CombatLogRow":
            print(f"❌ read_all() must return list[CombatLogRow], got {type(rows[0])}")
            raise SystemExit(1)
        if rows[1].result != "win":
            print(f"❌ Second row result should be 'win', got {rows[1].result!r}")
            raise SystemExit(1)

        # --- CsvCombatLogRepository (ported from Mission 06) ---
        csv_path = Path(tmp) / "combat_log.csv"
        try:
            csv_repo = CsvCombatLogRepository(csv_path)
        except NotImplementedError:
            print("❌ CsvCombatLogRepository.__init__() is not implemented yet.")
            raise SystemExit(1)

        try:
            csv_empty = csv_repo.read_all()
        except NotImplementedError:
            print("❌ CsvCombatLogRepository.read_all() is not implemented yet.")
            raise SystemExit(1)
        if csv_empty != []:
            print(f"❌ CsvCombatLogRepository.read_all() before any append should return [], got {csv_empty}")
            raise SystemExit(1)

        try:
            csv_repo.append(row)
        except NotImplementedError:
            print("❌ CsvCombatLogRepository.append() is not implemented yet.")
            raise SystemExit(1)
        csv_repo.append(row2)

        csv_rows = csv_repo.read_all()
        if len(csv_rows) != 2:
            print(f"❌ Expected 2 CSV rows after two appends, got {len(csv_rows)}")
            raise SystemExit(1)
        if type(csv_rows[0]).__name__ != "CombatLogRow":
            print(f"❌ CsvCombatLogRepository.read_all() must return list[CombatLogRow], got {type(csv_rows[0])}")
            raise SystemExit(1)
        if csv_rows[0].damage_dealt != 20:
            print(f"❌ First CSV row damage_dealt should be 20, got {csv_rows[0].damage_dealt}")
            raise SystemExit(1)
        if csv_rows[1].result != "win":
            print(f"❌ Second CSV row result should be 'win', got {csv_rows[1].result!r}")
            raise SystemExit(1)

    print("✅ Boss Fight complete — JSON and SQLite backends both satisfy the same contract.")
    print("   The game code doesn't know which backend is running. That's the point.")
    update_progress("03_sqlite_repository_backend")


if __name__ == "__main__":
    main()
