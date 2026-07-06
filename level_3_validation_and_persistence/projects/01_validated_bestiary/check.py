"""check.py — Project 01: Validated Bestiary"""

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


def _write_temp_json(records: list) -> Path:
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    json.dump(records, tmp)
    tmp.close()
    return Path(tmp.name)


def main() -> None:
    # ── 1. Import ─────────────────────────────────────────────────────────────
    try:
        from pydantic import BaseModel

        from task import MonsterDomain, MonsterModel, load_bestiary, to_domain
    except ImportError as exc:
        print(f"❌ Cannot import from task.py: {exc}")
        raise SystemExit(1)

    # ── 2. MonsterModel is a Pydantic BaseModel ───────────────────────────────
    if not issubclass(MonsterModel, BaseModel):
        print("❌ MonsterModel must be a Pydantic BaseModel subclass")
        raise SystemExit(1)
    for field in ("name", "hp", "attack_type", "gold"):
        if field not in MonsterModel.model_fields:
            print(f"❌ MonsterModel must have field '{field}'")
            raise SystemExit(1)
    print("✓ MonsterModel is a Pydantic BaseModel with required fields")

    # ── 3. Scaffold guard ─────────────────────────────────────────────────────
    valid_record = [{"name": "Goblin", "hp": 30, "attack_type": "melee", "gold": 5}]
    path = _write_temp_json(valid_record)
    try:
        result = load_bestiary(path)
    except NotImplementedError:
        print("❌ task.py is not implemented yet — replace NotImplementedError with real code")
        raise SystemExit(1)
    finally:
        path.unlink(missing_ok=True)

    # ── 4. load_bestiary returns a 2-tuple ────────────────────────────────────
    if not (isinstance(result, tuple) and len(result) == 2):
        print(f"❌ load_bestiary() must return a 2-tuple, got {type(result)}")
        raise SystemExit(1)
    monsters, errors = result
    if not isinstance(monsters, list) or not isinstance(errors, list):
        print("❌ load_bestiary() must return (list, list)")
        raise SystemExit(1)
    print("✓ load_bestiary() returns a 2-tuple (monsters, errors)")

    # ── 5. to_domain converts model to non-Pydantic object ───────────────────
    try:
        model = MonsterModel(name="Goblin", hp=30, attack_type="melee", gold=5)
        domain = to_domain(model)
    except NotImplementedError:
        print("❌ to_domain() not implemented")
        raise SystemExit(1)
    if isinstance(domain, BaseModel):
        print("❌ to_domain() must return a plain Python object, not a Pydantic model")
        raise SystemExit(1)
    for attr in ("name", "hp", "attack_type", "gold"):
        if not hasattr(domain, attr):
            print(f"❌ to_domain() result must have attribute '{attr}'")
            raise SystemExit(1)
    assert domain.name == "Goblin" and domain.hp == 30, (
        f"to_domain() produced wrong values: {domain}"
    )
    print("✓ to_domain() returns a plain Python object with correct field values")

    # ── 6. Valid records go to monsters list ──────────────────────────────────
    valid_records = [
        {"name": "Goblin", "hp": 30, "attack_type": "melee", "gold": 5},
        {"name": "Archer", "hp": 25, "attack_type": "ranged", "gold": 8},
    ]
    path = _write_temp_json(valid_records)
    try:
        ok, errs = load_bestiary(path)
    finally:
        path.unlink(missing_ok=True)
    if len(ok) != 2:
        print(f"❌ 2 valid records should produce 2 domain objects, got {len(ok)}")
        raise SystemExit(1)
    if len(errs) != 0:
        print(f"❌ 2 valid records should produce 0 errors, got {len(errs)}")
        raise SystemExit(1)
    for obj in ok:
        if isinstance(obj, BaseModel):
            print("❌ monsters list must contain plain Python objects, not Pydantic models")
            raise SystemExit(1)
    print(f"✓ Valid records → monsters list (2 objects, 0 errors)")

    # ── 7. Invalid records go to errors list (not monsters list) ─────────────
    bad_records = [
        {"name": "Troll", "hp": -10, "attack_type": "melee", "gold": 5},   # negative hp
        {"name": "Ghost", "hp": 0,   "attack_type": "melee", "gold": 0},   # zero hp
        {"name": "Shade", "hp": 20,  "attack_type": "shadow", "gold": 0},  # bad attack_type
        {"name": "Demon", "hp": 50,  "attack_type": "magic",  "gold": -1}, # negative gold
        {"name": "",      "hp": 40,  "attack_type": "melee",  "gold": 5},  # empty name
    ]
    path = _write_temp_json(bad_records)
    try:
        ok, errs = load_bestiary(path)
    finally:
        path.unlink(missing_ok=True)
    if len(ok) != 0:
        print(f"❌ 5 invalid records should produce 0 domain objects, got {len(ok)}")
        raise SystemExit(1)
    if len(errs) != 5:
        print(f"❌ 5 invalid records should produce 5 error messages, got {len(errs)}")
        print("   Hint: empty name (\"\") must be rejected — add Field(min_length=1) to MonsterModel.name")
        raise SystemExit(1)
    for msg in errs:
        if not isinstance(msg, str) or len(msg.strip()) == 0:
            print("❌ Error messages must be non-empty strings")
            raise SystemExit(1)
    print(f"✓ Invalid records → errors list ({len(errs)} messages, 0 domain objects, including empty name)")

    # ── 8. Mixed batch — bad record does not stop valid ones ──────────────────
    mixed = [
        {"name": "Goblin", "hp": 30,  "attack_type": "melee", "gold": 5},
        {"name": "Troll",  "hp": -10, "attack_type": "melee", "gold": 5},  # bad
        {"name": "Dragon", "hp": 200, "attack_type": "magic",  "gold": 50},
    ]
    path = _write_temp_json(mixed)
    try:
        ok, errs = load_bestiary(path)
    finally:
        path.unlink(missing_ok=True)
    if len(ok) != 2:
        print(f"❌ Mixed batch: expected 2 valid, got {len(ok)}")
        raise SystemExit(1)
    if len(errs) != 1:
        print(f"❌ Mixed batch: expected 1 error, got {len(errs)}")
        raise SystemExit(1)
    print("✓ Mixed batch: invalid record does not prevent loading valid ones")

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("01_validated_bestiary")
    print()
    print("✅ Project 01 complete: Validated Bestiary works!")
    print()
    print("   Pydantic validates at the boundary — the game only sees clean data.")
    print("   Bad records are collected, not silenced. That is production-grade loading.")


if __name__ == "__main__":
    main()
