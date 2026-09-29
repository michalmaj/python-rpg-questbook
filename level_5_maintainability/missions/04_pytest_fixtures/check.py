"""Check: Mission 04 — pytest fixtures.

Structural checks confirm the required fixtures exist and the factory
fixture is actually called somewhere. The real proof of competence is
behavioral: the student's test suite must pass against the correct
rpg.py, then must FAIL against each of six independent, single-behavior
mutants — one per behavior the mission's own README asks the student to
test (damage formula, damage floor, take_damage, potion heal, empty
potions, simulate_turn's hero-wins path). A suite of fixtures that are
never used, or tests that assert nothing, kills none of these mutants.
"""

import ast
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

mission = Path(__file__).parent
conftest = mission / "conftest.py"
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
            [sys.executable, "-m", "pytest", str(mission), "-q", "--tb=line"],
            capture_output=True, text=True, cwd=str(mission), env=env,
        )
    finally:
        _clear_pycache()


# ── conftest.py has the three required fixtures ───────────────────────────────

if not conftest.exists():
    print("❌ conftest.py not found")
    raise SystemExit(1)
conf_src = conftest.read_text()
fixture_count = sum(
    1 for ln in conf_src.splitlines()
    if "@pytest.fixture" in ln and not ln.lstrip().startswith("#")
)
if fixture_count < 3:
    print(f"❌ Only {fixture_count} @pytest.fixture found in conftest.py (need >= 3)")
    raise SystemExit(1)
for fname in ("warrior", "goblin", "make_hero"):
    if f"def {fname}" not in conf_src:
        print(f"❌ Fixture '{fname}' not found in conftest.py")
        raise SystemExit(1)
print(f"✓ conftest.py has {fixture_count} fixtures (warrior, goblin, make_hero)")

# ── test_combat.py has tests, and the make_hero factory is actually called ───

if not test_file.exists():
    print("❌ test_combat.py not found")
    raise SystemExit(1)
test_src = test_file.read_text()
test_count = sum(
    1 for ln in test_src.splitlines()
    if "def test_" in ln and not ln.lstrip().startswith("#")
)
if test_count < 5:
    print(f"❌ Only {test_count} test_ functions found in test_combat.py (need >= 5)")
    raise SystemExit(1)
print(f"✓ test_combat.py has {test_count} test functions")

try:
    test_tree = ast.parse(test_src)
except SyntaxError as e:
    print(f"❌ test_combat.py has a syntax error: {e}")
    raise SystemExit(1)
make_hero_called = any(
    isinstance(node, ast.Call)
    and isinstance(node.func, ast.Name)
    and node.func.id == "make_hero"
    for node in ast.walk(test_tree)
)
if not make_hero_called:
    print("❌ The make_hero factory fixture is never called (e.g. make_hero(potions=0)) "
          "— accepting it as a parameter is not enough, a test must actually use it")
    raise SystemExit(1)
print("✓ make_hero factory fixture is actually called in a test")

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
print("✓ All tests pass against the correct rpg.py")

# ── Gate 2: the suite must FAIL against each single-behavior mutant ──────────
#
# Each mutant breaks exactly one behavior the README asks the student to
# test. A test suite that passes on all six mutants isn't testing anything —
# it's just checking that rpg.py imports.

MUTANTS: list[tuple[str, str, str]] = [
    (
        "compute_damage: minimum-damage floor removed",
        "    return max(1, atk + roll - def_)",
        "    return atk + roll - def_",
    ),
    (
        "compute_damage: formula uses the wrong sign for roll",
        "    return max(1, atk + roll - def_)",
        "    return max(1, atk - roll - def_)",
    ),
    (
        "Hero.take_damage: amount is ignored",
        "    def take_damage(self, amount: int) -> None:\n        self.hp = max(0, self.hp - amount)\n\n    def use_potion",
        "    def take_damage(self, amount: int) -> None:\n        self.hp = max(0, self.hp)\n\n    def use_potion",
    ),
    (
        "Hero.use_potion: heal amount is zero",
        "        self.hp = min(self.hp + 30, self.max_hp)",
        "        self.hp = min(self.hp + 0, self.max_hp)",
    ),
    (
        "Hero.use_potion: empty-potions guard disabled",
        "        if self.potions <= 0:\n            return False",
        "        if False:\n            return False",
    ),
    (
        "simulate_turn: hero's attack deals zero damage",
        "    hero_dmg = compute_damage(hero.atk, monster.def_, hero_roll)\n    monster.take_damage(hero_dmg)",
        "    hero_dmg = compute_damage(hero.atk, monster.def_, hero_roll)\n    monster.take_damage(0)",
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
            print("   A correct test suite for this mission must fail when this "
                  "behavior breaks — add or fix a test that exercises it.")
            raise SystemExit(1)
        print(f"✓ tests correctly fail when: {label}")
finally:
    rpg_file.write_text(original_rpg_src)
    _clear_pycache()

if rpg_file.read_text() != original_rpg_src:
    print("❌ internal check error: rpg.py was not restored correctly — please re-run")
    raise SystemExit(1)

update_progress("04_pytest_fixtures")
print("\n✅ Mission 04 complete!")
