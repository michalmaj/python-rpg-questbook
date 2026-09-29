"""Check: Mission 05 — pytest parametrize.

Structural checks confirm parametrize is used, ids= is present, and each
parametrized test actually references its own parameters in the body (not
just in the decorator). The real proof is behavioral: the suite must pass
against the correct rpg.py, then FAIL against each of four independent
single-behavior mutants — one per case the README's own parametrize tables
ask the student to cover (compute_damage's normal/minimum/maximum cases,
and simulate_turn's hero-wins/hero-loses outcomes). Parametrize decorated
with beautiful ids= but a body that ignores its parameters kills none of
these mutants.
"""

import ast
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

mission = Path(__file__).parent
test_file = mission / "test_combat.py"
rpg_file = mission / "rpg.py"
PROGRESS_FILE = Path(__file__).parents[2] / ".progress"


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
    shutil.rmtree(mission / "__pycache__", ignore_errors=True)


def _run_pytest() -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    _clear_pycache()
    try:
        return subprocess.run(
            [sys.executable, "-m", "pytest", str(mission), "-v", "--tb=line"],
            capture_output=True, text=True, cwd=str(mission), env=env,
        )
    finally:
        _clear_pycache()


# ── test_combat.py exists ──────────────────────────────────────────────────────

if not test_file.exists():
    print("❌ test_combat.py not found")
    raise SystemExit(1)
src = test_file.read_text()

# ── @pytest.mark.parametrize used >= 2 times ──────────────────────────────────

param_count = sum(
    1 for ln in src.splitlines()
    if "@pytest.mark.parametrize" in ln and not ln.lstrip().startswith("#")
)
if param_count < 2:
    print(f"❌ Only {param_count} @pytest.mark.parametrize found (need >= 2)")
    raise SystemExit(1)
print(f"✓ {param_count} @pytest.mark.parametrize decorators found")

# ── ids= used in at least one parametrize call ────────────────────────────────

if not any(
    "ids=" in ln and not ln.lstrip().startswith("#")
    for ln in src.splitlines()
):
    print("❌ ids= not found — add ids=[...] to at least one @pytest.mark.parametrize call")
    raise SystemExit(1)
print("✓ ids= used in at least one parametrize call")

# ── each parametrized test references its own parameters in the body ─────────

try:
    tree = ast.parse(src)
except SyntaxError as e:
    print(f"❌ test_combat.py has a syntax error: {e}")
    raise SystemExit(1)


def _parametrize_param_names(call: ast.Call) -> list[str]:
    if not call.args:
        return []
    first = call.args[0]
    if isinstance(first, ast.Constant) and isinstance(first.value, str):
        return [p.strip() for p in first.value.split(",") if p.strip()]
    return []


def _names_used_in_body(func: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    used: set[str] = set()
    for stmt in func.body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Name):
                used.add(node.id)
    return used


checked_any = False
for node in ast.walk(tree):
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        continue
    for dec in node.decorator_list:
        if not (isinstance(dec, ast.Call) and "parametrize" in ast.unparse(dec.func)):
            continue
        checked_any = True
        param_names = _parametrize_param_names(dec)
        if not param_names:
            continue
        used = _names_used_in_body(node)
        if not any(p in used for p in param_names):
            print(f"❌ {node.name}(): none of its parametrize parameters "
                  f"({param_names}) are referenced in the test body — a test "
                  f"that ignores its own parameters isn't testing them")
            raise SystemExit(1)
if checked_any:
    print("✓ parametrized tests reference their own parameters")

# ── Gate 1: the suite must pass against the real, correct rpg.py ─────────────

if not rpg_file.exists():
    print("❌ rpg.py not found")
    raise SystemExit(1)
original_rpg_src = rpg_file.read_text()

result = _run_pytest()
if result.returncode != 0:
    print("❌ pytest fails against the correct rpg.py:")
    print(result.stdout[-3000:])
    raise SystemExit(1)

collected = [ln for ln in result.stdout.splitlines() if " PASSED" in ln]
if len(collected) < 8:
    print(f"❌ Only {len(collected)} test cases collected (need >= 8, parametrize "
          f"should multiply them)")
    raise SystemExit(1)
print(f"✓ {len(collected)} test cases pass against the correct rpg.py "
      f"(including parametrized cases)")

# ── Gate 2: the suite must FAIL against each single-behavior mutant ──────────
#
# One mutant per case the README's own parametrize tables ask the student to
# cover: compute_damage's normal/maximum cases (sign flip breaks both),
# compute_damage's minimum-damage floor, and simulate_turn's two outcomes.

MUTANTS: list[tuple[str, str, str]] = [
    (
        "compute_damage: minimum-damage floor removed (breaks the min_damage case)",
        "    return max(1, atk + roll - def_)",
        "    return atk + roll - def_",
    ),
    (
        "compute_damage: formula uses the wrong sign for roll "
        "(breaks the normal and max_hit cases)",
        "    return max(1, atk + roll - def_)",
        "    return max(1, atk - roll - def_)",
    ),
    (
        "simulate_turn: hero's attack deals zero damage (breaks the hero-wins case)",
        "    hero_dmg = compute_damage(hero.atk, monster.def_, hero_roll)\n    monster.take_damage(hero_dmg)",
        "    hero_dmg = compute_damage(hero.atk, monster.def_, hero_roll)\n    monster.take_damage(0)",
    ),
    (
        "simulate_turn: monster's counterattack deals zero damage "
        "(breaks the hero-loses case)",
        "    monster_dmg = compute_damage(monster.atk, hero.def_, monster_roll)\n    hero.take_damage(monster_dmg)",
        "    monster_dmg = compute_damage(monster.atk, hero.def_, monster_roll)\n    hero.take_damage(0)",
    ),
]

try:
    for label, old, new in MUTANTS:
        if old not in original_rpg_src:
            print(f"❌ internal check error: mutant anchor not found for: {label}")
            raise SystemExit(1)
        rpg_file.write_text(original_rpg_src.replace(old, new, 1))
        result = _run_pytest()
        if result.returncode == 0:
            print(f"❌ Your tests did not catch this bug: {label}.")
            print("   Add or extend a parametrize case that exercises it.")
            raise SystemExit(1)
        print(f"✓ tests correctly fail when: {label}")
finally:
    rpg_file.write_text(original_rpg_src)
    _clear_pycache()

if rpg_file.read_text() != original_rpg_src:
    print("❌ internal check error: rpg.py was not restored correctly — please re-run")
    raise SystemExit(1)

update_progress("05_pytest_parametrize")
print("\n✅ Mission 05 complete!")
