"""Check: Data Recall Checkpoint — Combat Log Analytics.

Behavioral checker: every function is run against TWO fixtures (primary and
variant) and compared against ground truth computed independently with
stdlib `csv` + plain Python — never by re-running the student's own pandas
or NumPy code. The variant fixture has a genuinely different win-rate
ranking and different damage statistics, so a hardcoded answer that happens
to match the primary fixture fails on the variant.

For win_rate_by_class and damage_stats, Pandas' `groupby` and NumPy's array
work are explicit learning objectives for this checkpoint (not just "produce
the right numbers") — so those two functions also get a light technique
gate on top of the behavioral one: an AST check that `groupby` is actually
called inside win_rate_by_class, and a monkeypatch spy confirming that
`numpy.percentile` or `numpy.quantile` (equivalent APIs for the same
75th-percentile computation) is actually called inside damage_stats.
Neither gate cares about variable names, chaining style, or lambda usage.
"""
import ast
import csv
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
mission = Path(__file__).parent
PROGRESS_FILE = Path(__file__).parent / ".progress"


def update_progress() -> None:
    progress: dict = {"missions": {}, "projects": {}}
    if PROGRESS_FILE.exists():
        try:
            progress = json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    progress["projects"]["data_recall_checkpoint"] = "complete"
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


# ── ground truth (stdlib csv + plain Python only — never pandas/numpy) ──────

def _load_raw_rows(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _ground_truth_win_rate_by(rows: list[dict], key: str) -> dict[str, float]:
    totals: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for row in rows:
        if row["result"] in ("win", "loss"):
            totals[row[key]][1] += 1
            if row["result"] == "win":
                totals[row[key]][0] += 1
    return {k: wins / total for k, (wins, total) in totals.items() if total > 0}


def _percentile_linear(sorted_values: list[float], pct: float) -> float:
    n = len(sorted_values)
    if n == 0:
        return 0.0
    k = (n - 1) * (pct / 100)
    f = int(k)
    c = f + 1 if f + 1 < n else f
    if f == c:
        return float(sorted_values[f])
    d0 = sorted_values[f] * (c - k)
    d1 = sorted_values[c] * (k - f)
    return float(d0 + d1)


def _ground_truth_damage_stats(rows: list[dict]) -> dict[str, float | int]:
    values = [int(row["damage_dealt"]) for row in rows if row["action"] == "attack"]
    mean = statistics.mean(values)
    std = statistics.pstdev(values)
    p75 = _percentile_linear(sorted(values), 75)
    high_count = sum(1 for v in values if v > p75)
    return {"mean": mean, "std": std, "p75": p75, "high_damage_count": high_count}


def _ground_truth_ranking(rows: list[dict]) -> list[str]:
    rates = _ground_truth_win_rate_by(rows, "monster")
    return [name for name, _ in sorted(rates.items(), key=lambda kv: kv[1])]


def _dicts_close(actual: dict, expected: dict, *, rel_tol: float = 1e-6, abs_tol: float = 1e-6) -> bool:
    if set(actual.keys()) != set(expected.keys()):
        return False
    for k, exp_v in expected.items():
        act_v = actual.get(k)
        if isinstance(exp_v, float) or isinstance(act_v, float):
            if act_v is None or not math.isclose(float(act_v), float(exp_v), rel_tol=rel_tol, abs_tol=abs_tol):
                return False
        else:
            if act_v != exp_v:
                return False
    return True


# ── AST technique gate: win_rate_by_class must call .groupby(...) ───────────

def _function_uses_attr_call(source: str, fn_name: str, attr_name: str) -> bool:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or node.name != fn_name:
            continue
        for child in ast.walk(node):
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
                if child.func.attr == attr_name:
                    return True
    return False


FIXTURES = [
    ("primary", mission / "data" / "combat_log_fixture.csv"),
    ("variant", mission / "data" / "combat_log_fixture_variant.csv"),
]


def main() -> None:
    try:
        from task import (  # type: ignore[import]
            load_combat_log,
            win_rate_by_class,
            damage_stats,
            rank_monsters_by_difficulty,
        )
    except ImportError as exc:
        print(f"❌ Cannot import from task.py: {exc}")
        raise SystemExit(1)

    import pandas as pd

    # ── scaffold guard ────────────────────────────────────────────────────
    try:
        load_combat_log(FIXTURES[0][1])
    except NotImplementedError:
        print("❌ load_combat_log is not implemented yet — replace NotImplementedError with your code")
        raise SystemExit(1)
    except Exception:
        pass  # any real error = student modified it; continue to the real checks

    for fixture_name, fixture_path in FIXTURES:
        raw_rows = _load_raw_rows(fixture_path)

        # ── Task 1: load_combat_log ─────────────────────────────────────
        df = load_combat_log(fixture_path)
        if not isinstance(df, pd.DataFrame):
            print(f"❌ [{fixture_name}] load_combat_log must return a pandas DataFrame, got {type(df)}")
            raise SystemExit(1)
        if len(df) != len(raw_rows):
            print(f"❌ [{fixture_name}] load_combat_log: expected {len(raw_rows)} rows, got {len(df)}")
            raise SystemExit(1)
        expected_columns = {
            "battle_id", "turn", "hero_name", "hero_class", "monster",
            "action", "damage_dealt", "damage_taken", "hero_hp", "monster_hp", "result",
        }
        if not expected_columns.issubset(set(df.columns)):
            print(f"❌ [{fixture_name}] load_combat_log: missing columns "
                  f"{expected_columns - set(df.columns)}")
            raise SystemExit(1)
        if not pd.api.types.is_integer_dtype(df["damage_dealt"]):
            print(f"❌ [{fixture_name}] load_combat_log: 'damage_dealt' should be numeric "
                  f"(did you read the CSV with pandas, not row-by-row strings?)")
            raise SystemExit(1)
        print(f"✓ [{fixture_name}] load_combat_log → DataFrame, {len(df)} rows, correct columns")

        # ── Task 2: win_rate_by_class (behavior + groupby technique gate) ─
        result = win_rate_by_class(df)
        expected = _ground_truth_win_rate_by(raw_rows, "hero_class")
        if not isinstance(result, dict) or not _dicts_close(result, expected):
            print(f"❌ [{fixture_name}] win_rate_by_class: expected {expected}, got {result}")
            raise SystemExit(1)
        print(f"✓ [{fixture_name}] win_rate_by_class → {result}")

        # ── Task 3: damage_stats (behavior + percentile technique gate) ────
        # np.percentile and np.quantile are equivalent NumPy APIs for the
        # same 75th-percentile computation (README describes the operation,
        # not one specific function name) — either one counts.
        import numpy as np
        _percentile_used = False
        _original_percentile = np.percentile
        _original_quantile = np.quantile

        def _percentile_spy(*args, **kwargs):
            nonlocal _percentile_used
            _percentile_used = True
            return _original_percentile(*args, **kwargs)

        def _quantile_spy(*args, **kwargs):
            nonlocal _percentile_used
            _percentile_used = True
            return _original_quantile(*args, **kwargs)

        np.percentile = _percentile_spy
        np.quantile = _quantile_spy
        try:
            result = damage_stats(df)
        finally:
            np.percentile = _original_percentile
            np.quantile = _original_quantile

        expected = _ground_truth_damage_stats(raw_rows)
        if not isinstance(result, dict) or not _dicts_close(result, expected, rel_tol=1e-3, abs_tol=1e-3):
            print(f"❌ [{fixture_name}] damage_stats: expected {expected}, got {result}")
            raise SystemExit(1)
        if not _percentile_used:
            print(f"❌ [{fixture_name}] damage_stats: neither np.percentile nor np.quantile "
                  f"was called — values must be computed with NumPy, not plain Python "
                  f"arithmetic on a ceremonially-created array")
            raise SystemExit(1)
        print(f"✓ [{fixture_name}] damage_stats → {result} (np.percentile/np.quantile confirmed used)")

        # ── Task 4: rank_monsters_by_difficulty (behavior) ─────────────────
        result = rank_monsters_by_difficulty(df)
        expected = _ground_truth_ranking(raw_rows)
        if list(result) != expected:
            print(f"❌ [{fixture_name}] rank_monsters_by_difficulty: expected {expected}, got {result}")
            raise SystemExit(1)
        print(f"✓ [{fixture_name}] rank_monsters_by_difficulty → {result}")

    # ── technique gate: win_rate_by_class must actually use groupby ──────
    src = (mission / "task.py").read_text()
    if not _function_uses_attr_call(src, "win_rate_by_class", "groupby"):
        print("❌ win_rate_by_class must use pandas' groupby — "
              "a per-class Python loop (e.g. `for cls in df['hero_class'].unique(): ...`) "
              "produces the same numbers but skips the learning objective of this task")
        raise SystemExit(1)
    print("✓ win_rate_by_class uses pandas groupby")

    update_progress()
    print("\n✅ Data Recall Checkpoint complete! Pandas and NumPy are back online.")


if __name__ == "__main__":
    main()
