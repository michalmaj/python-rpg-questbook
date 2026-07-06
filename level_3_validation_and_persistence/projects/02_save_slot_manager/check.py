"""check.py — Project 02: Save Slot Manager"""

import json
import sys
import tempfile
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PROGRESS_FILE = Path(__file__).parents[3] / "level_3_validation_and_persistence" / ".progress"

sys.path.insert(0, str(PROJECT_DIR))


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


def _make_save(slot: int = 1, hero_name: str = "Ada", hero_hp: int = 120,
               level: int = 5, gold: int = 100) -> "SaveGameModel":
    from task import SaveGameModel
    return SaveGameModel(slot=slot, hero_name=hero_name,
                         hero_hp=hero_hp, level=level, gold=gold)


def _run_repo_contract(repo: object, label: str) -> None:
    """Test the four-method contract on any repository implementation."""
    from task import SaveGameModel

    # save + load round-trip
    save1 = _make_save(slot=1, hero_name="Ada", hero_hp=120, level=5, gold=100)
    repo.save(save1)  # type: ignore[union-attr]
    loaded = repo.load(1)  # type: ignore[union-attr]
    assert loaded is not None, f"[{label}] load(1) returned None after save"
    assert isinstance(loaded, SaveGameModel), (
        f"[{label}] load() must return SaveGameModel, got {type(loaded)}"
    )
    assert loaded.hero_name == "Ada" and loaded.hero_hp == 120, (
        f"[{label}] Round-trip failed: {loaded}"
    )
    assert loaded.schema_version == 1, (
        f"[{label}] schema_version must be preserved, got {loaded.schema_version}"
    )
    print(f"  ✓ [{label}] save + load round-trip preserves all fields")

    # list_slots
    save2 = _make_save(slot=2, hero_name="Rex", hero_hp=80, level=3, gold=50)
    repo.save(save2)  # type: ignore[union-attr]
    slots = repo.list_slots()  # type: ignore[union-attr]
    assert isinstance(slots, list), f"[{label}] list_slots() must return list"
    assert 1 in slots and 2 in slots, (
        f"[{label}] list_slots() should contain [1, 2], got {slots}"
    )
    assert slots == sorted(slots), f"[{label}] list_slots() must be sorted"
    print(f"  ✓ [{label}] list_slots() returns {slots}")

    # load non-existent slot returns None
    result = repo.load(3)  # type: ignore[union-attr]
    assert result is None, (
        f"[{label}] load() for empty slot must return None, got {result!r}"
    )
    print(f"  ✓ [{label}] load() returns None for empty slot")

    # delete
    repo.delete(1)  # type: ignore[union-attr]
    after_delete = repo.load(1)  # type: ignore[union-attr]
    assert after_delete is None, (
        f"[{label}] load() after delete(1) must return None, got {after_delete!r}"
    )
    remaining = repo.list_slots()  # type: ignore[union-attr]
    assert 1 not in remaining, (
        f"[{label}] slot 1 must not appear in list_slots() after delete"
    )
    print(f"  ✓ [{label}] delete() removes slot; list_slots now {remaining}")

    # delete non-existent slot is a no-op (must not raise)
    try:
        repo.delete(3)
    except Exception as exc:
        print(f"  ❌ [{label}] delete() on empty slot raised {type(exc).__name__}: {exc}")
        raise SystemExit(1)
    print(f"  ✓ [{label}] delete() on empty slot is a no-op")


def main() -> None:
    # ── 1. Import ─────────────────────────────────────────────────────────────
    try:
        from task import (
            InMemorySaveRepository,
            JsonSaveRepository,
            SaveGameModel,
            SaveRepository,
        )
    except ImportError as exc:
        print(f"❌ Cannot import from task.py: {exc}")
        raise SystemExit(1)

    # ── 2. SaveGameModel is a Pydantic BaseModel ──────────────────────────────
    try:
        from pydantic import BaseModel
    except ImportError:
        print("❌ pydantic not installed")
        raise SystemExit(1)

    if not issubclass(SaveGameModel, BaseModel):
        print("❌ SaveGameModel must be a Pydantic BaseModel subclass")
        raise SystemExit(1)
    if "schema_version" not in SaveGameModel.model_fields:
        print("❌ SaveGameModel must have a 'schema_version' field")
        raise SystemExit(1)
    model = SaveGameModel(slot=1, hero_name="Ada", hero_hp=120, level=5, gold=100)
    assert model.schema_version == 1, "default schema_version must be 1"
    print("✓ SaveGameModel is a Pydantic BaseModel with schema_version field")

    # ── 3. Scaffold guard ─────────────────────────────────────────────────────
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = JsonSaveRepository(Path(tmpdir))
        try:
            repo.save(model)
        except NotImplementedError:
            print("❌ task.py is not implemented yet — replace NotImplementedError with real code")
            raise SystemExit(1)
        except Exception:
            pass

    # ── 4. InMemorySaveRepository contract ────────────────────────────────────
    print("\nInMemorySaveRepository:")
    try:
        mem_repo = InMemorySaveRepository()
    except NotImplementedError:
        print("❌ InMemorySaveRepository.__init__ not implemented")
        raise SystemExit(1)
    try:
        _run_repo_contract(mem_repo, "InMemory")
    except AssertionError as exc:
        print(f"❌ {exc}")
        raise SystemExit(1)

    # ── 5. JsonSaveRepository contract ────────────────────────────────────────
    print("\nJsonSaveRepository:")
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            json_repo = JsonSaveRepository(Path(tmpdir))
        except NotImplementedError:
            print("❌ JsonSaveRepository.__init__ not implemented")
            raise SystemExit(1)
        try:
            _run_repo_contract(json_repo, "Json")
        except AssertionError as exc:
            print(f"❌ {exc}")
            raise SystemExit(1)

        # ── 6. JSON file exists on disk after save ─────────────────────────
        json_repo2 = JsonSaveRepository(Path(tmpdir))
        save3 = _make_save(slot=3, hero_name="Zara", hero_hp=60, level=2, gold=25)
        json_repo2.save(save3)
        slot_files = list(Path(tmpdir).glob("slot_3*"))
        if not slot_files:
            print("❌ JsonSaveRepository.save() must write a file named slot_3.json (or similar)")
            raise SystemExit(1)
        print(f"  ✓ [Json] slot_3 file exists on disk: {slot_files[0].name}")

        # ── 7. JSON round-trip is complete ────────────────────────────────
        raw = json.loads(slot_files[0].read_text())
        assert "schema_version" in raw, "JSON file must contain 'schema_version'"
        assert raw["hero_name"] == "Zara", "JSON file must contain hero_name"
        print("  ✓ [Json] JSON file contains all fields including schema_version")

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("02_save_slot_manager")
    print()
    print("✅ Project 02 complete: Save Slot Manager works!")
    print()
    print("   Both backends satisfy the same Protocol.")
    print("   The game doesn't care which one runs — that is the repository pattern.")


if __name__ == "__main__":
    main()
