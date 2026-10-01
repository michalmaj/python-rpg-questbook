# level_6_api/missions/07_api_tests/check.py
"""Check: Mission 07 — API Tests.

Structural checks confirm TestClient and dependency_overrides are used, no
mocking, and at least 6 test functions exist. The real proof of competence is
behavioral: the student's test suite must pass against the correct
application, then FAIL against each of six independent, single-behavior
mutants — one per test the mission's own README asks the student to write
(health status, monster list, battle winner, invalid-monster 404, session
round-trip, session-not-found 404). A suite of tests that make real requests
but assert nothing meaningful (`assert True`) kills none of these mutants.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROGRESS_FILE = Path(__file__).parents[2] / ".progress"
mission = Path(__file__).parent


def update_progress(mission_id: str) -> None:
    progress: dict = {"missions": {}, "projects": {}}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    progress["missions"][mission_id] = "complete"
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


def _clear_pycache() -> None:
    for d in mission.rglob("__pycache__"):
        shutil.rmtree(d, ignore_errors=True)


def _run_pytest() -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(mission)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    _clear_pycache()
    try:
        return subprocess.run(
            [sys.executable, "-m", "pytest", "task/tests/test_api.py", "-q", "--tb=line"],
            capture_output=True, text=True, cwd=str(mission), env=env,
        )
    finally:
        _clear_pycache()


# ── test file exists ──────────────────────────────────────────────────────────

test_file = mission / "task/tests/test_api.py"
if not test_file.exists():
    print("❌ task/tests/test_api.py not found — create your test file")
    raise SystemExit(1)

src = test_file.read_text()

# ── TestClient used ───────────────────────────────────────────────────────────

if "TestClient" not in src:
    print("❌ TestClient not used in test_api.py")
    raise SystemExit(1)
print("✓ TestClient used in test_api.py")

# ── dependency_overrides used (session isolation) ─────────────────────────────

if "dependency_overrides" not in src:
    print("❌ app.dependency_overrides not used — isolate SessionRepository in tests with tmp_path")
    raise SystemExit(1)
print("✓ dependency_overrides used for test isolation")

# ── no unittest.mock or @patch ────────────────────────────────────────────────

code_lines = [ln for ln in src.splitlines() if not ln.lstrip().startswith("#")]
code_src = "\n".join(code_lines)
if "unittest.mock" in code_src or "@patch" in code_src:
    print("❌ unittest.mock / @patch found — use app.dependency_overrides instead")
    raise SystemExit(1)
print("✓ No unittest.mock or @patch — clean dependency_overrides approach")

# ── at least 6 test functions ─────────────────────────────────────────────────

test_fn_count = sum(
    1 for ln in src.splitlines()
    if ln.lstrip().startswith("def test_") and not ln.lstrip().startswith("#")
)
if test_fn_count < 6:
    print(f"❌ Found {test_fn_count} test functions — write at least 6")
    raise SystemExit(1)
print(f"✓ {test_fn_count} test functions found")

# ── Gate 1: the suite must pass against the correct application ──────────────

result = _run_pytest()
if result.returncode != 0:
    print("❌ pytest fails against the correct application:")
    print(result.stdout[-2000:])
    print(result.stderr[-500:])
    raise SystemExit(1)
print("✓ All API tests pass against the correct application")

# ── Gate 2: the suite must FAIL against each single-behavior mutant ──────────
#
# One mutant per test the README asks for. Each is a real bug a client would
# notice; none of them touches anything not already covered by the mission's
# own 6 required behaviors. The hero-vs-Goblin matchup used in the mission's
# own test spec (warrior, atk=12/def_=6/hp=120 vs Goblin atk=8/def_=2/hp=30)
# is a guaranteed hero win regardless of dice rolls — worst case the hero
# takes 8 damage/round for at most 3 rounds (24 of 120 hp) while dealing a
# guaranteed kill to the goblin within 3 rounds — so asserting on the winner
# for that specific matchup is asserting a real invariant, not a coin flip.

MAIN_FILE = mission / "task/main.py"
MONSTERS_FILE = mission / "task/routers/monsters.py"
BATTLES_FILE = mission / "task/routers/battles.py"
SESSIONS_FILE = mission / "task/routers/sessions.py"

for path in (MAIN_FILE, MONSTERS_FILE, BATTLES_FILE, SESSIONS_FILE):
    if not path.exists():
        print(f"❌ {path.relative_to(mission)} not found")
        raise SystemExit(1)

originals = {p: p.read_text() for p in (MAIN_FILE, MONSTERS_FILE, BATTLES_FILE, SESSIONS_FILE)}

MUTANTS: list[tuple[str, Path, str, str]] = [
    (
        "health endpoint returns the wrong status",
        MAIN_FILE,
        '    return {"status": "ok"}',
        '    return {"status": "degraded"}',
    ),
    (
        "GET /monsters returns an empty list regardless of the catalog",
        MONSTERS_FILE,
        "    return [MonsterOut(name=m.name, hp=m.hp, atk=m.atk, defense=m.def_, gold=m.gold) for m in service.get_available_monsters()]",
        "    return []",
    ),
    (
        "POST /battle/simulate ignores the real outcome and always reports the monster winning "
        "(for Ada the warrior vs Goblin, the hero winning is a guaranteed outcome, not chance)",
        BATTLES_FILE,
        "    return BattleResultOut(**vars(result))",
        '    return BattleResultOut(hero_name=result.hero_name, monster_name=result.monster_name, winner="monster", rounds=result.rounds, gold_earned=result.gold_earned)',
    ),
    (
        "POST /battle/simulate with an unknown monster returns 200 instead of 404",
        BATTLES_FILE,
        "    try:\n        result = service.simulate(hero, req.monster_name)\n    except ValueError as exc:\n        raise HTTPException(status_code=404, detail=str(exc)) from exc",
        '    try:\n        result = service.simulate(hero, req.monster_name)\n    except ValueError:\n        return BattleResultOut(hero_name=hero.name, monster_name=req.monster_name, winner="hero", rounds=1, gold_earned=0)',
    ),
    (
        "POST /sessions returns a session_id but never actually saves the session "
        "(the GET half of the round-trip would then find nothing)",
        SESSIONS_FILE,
        "    session_id = str(uuid.uuid4())\n    session_repo.save(session_id, result)\n    return SessionCreated(session_id=session_id)",
        "    session_id = str(uuid.uuid4())\n    return SessionCreated(session_id=session_id)",
    ),
    (
        "GET /sessions/{id} returns 200 with a made-up result instead of 404 when the session doesn't exist",
        SESSIONS_FILE,
        '    result = session_repo.get(session_id)\n    if result is None:\n        raise HTTPException(status_code=404, detail=f"Session \'{session_id}\' not found")\n    return BattleResultOut(**vars(result))',
        '    result = session_repo.get(session_id)\n    if result is None:\n        return BattleResultOut(hero_name="Unknown", monster_name="Unknown", winner="hero", rounds=0, gold_earned=0)\n    return BattleResultOut(**vars(result))',
    ),
]

try:
    for label, path, old, new in MUTANTS:
        original_src = originals[path]
        if old not in original_src:
            print(f"❌ internal check error: mutant anchor not found for: {label}")
            raise SystemExit(1)
        path.write_text(original_src.replace(old, new, 1))
        result = _run_pytest()
        path.write_text(original_src)
        if result.returncode == 0:
            print(f"❌ Your tests did not catch this bug: {label}.")
            print("   A correct test suite for this mission must fail when this "
                  "behavior breaks — check the actual response data, not just the status code.")
            raise SystemExit(1)
        print(f"✓ tests correctly fail when: {label}")
finally:
    for path, original_src in originals.items():
        path.write_text(original_src)
    _clear_pycache()

for path, original_src in originals.items():
    if path.read_text() != original_src:
        print(f"❌ internal check error: {path.relative_to(mission)} was not restored correctly — please re-run")
        raise SystemExit(1)

update_progress("07_api_tests")
print("\n✅ Mission 07 complete!")
