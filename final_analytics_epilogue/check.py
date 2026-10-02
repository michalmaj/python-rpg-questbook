"""Check: Final Analytics Epilogue — Is the Game Balanced?

Behavioral checker: every function is run against TWO fixture pairs
(primary and variant — one pair for the deep-dive JSON, one pair for the
tournament-history CSV) and compared against ground truth computed
independently with stdlib `json`/`csv`/`statistics`/`math` — never by
re-running the student's own pandas or NumPy code. The variant fixtures
were generated from a genuinely different (but equally real) tournament
configuration, so hardcoded answers that happen to match the primary
fixtures fail on the variant.

NumPy array work (ndarray, reductions, percentile/quantile, boolean masks,
2D/axis aggregation) and Pandas `groupby` are explicit learning objectives
here (same precedent as the Data Recall Checkpoint) — so `deep_dive_stats`,
`battle_matrix_summary`, `win_rate_by_class`, `rank_monsters`, and
`unfavorable_matchups` each get a light technique gate on top of the
behavioral one. Every gate accepts multiple equivalent idioms (see
README) and never requires a specific variable name, chaining style, or
lambda form.
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
    progress["projects"]["final_analytics_epilogue"] = "complete"
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


# ── ground truth (stdlib json/csv/statistics/math only — never pandas/numpy) ─

def _percentile_linear(sorted_values: list[float], pct: float) -> float:
    n = len(sorted_values)
    if n == 0:
        return 0.0
    k = (n - 1) * (pct / 100)
    f = int(k)
    c = f + 1 if f + 1 < n else f
    if f == c:
        return float(sorted_values[f])
    return float(sorted_values[f] * (c - k) + sorted_values[c] * (k - f))


def _load_deep_dive_raw(path: Path) -> list[dict]:
    return json.loads(Path(path).read_text())["battles"]


def _ground_truth_deep_dive_stats(battles: list[dict]) -> dict[str, float | int]:
    wins = [1 if b["winner"] == "hero" else 0 for b in battles]
    rounds = [b["rounds"] for b in battles]
    quick = sum(1 for b in battles if b["winner"] == "hero" and b["rounds"] <= 2)
    return {
        "hero_win_rate": sum(wins) / len(wins),
        "median_rounds": statistics.median(rounds),
        "rounds_std": statistics.pstdev(rounds),
        "rounds_p90": _percentile_linear(sorted(rounds), 90),
        "quick_hero_wins": quick,
    }


def _ground_truth_matrix_summary(battles: list[dict]) -> dict[str, float]:
    wins = [1 if b["winner"] == "hero" else 0 for b in battles]
    rounds = [b["rounds"] for b in battles]
    return {"mean_win_indicator": statistics.mean(wins), "mean_rounds": statistics.mean(rounds)}


def _load_history_raw(path: Path) -> list[dict]:
    with Path(path).open(newline="") as f:
        return list(csv.DictReader(f))


def _grouped_mean(rows: list[dict], key: str) -> dict[str, float]:
    groups: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        groups[row[key]].append(float(row["hero_win_rate"]))
    return {k: statistics.mean(v) for k, v in groups.items()}


def _ground_truth_win_rate_by_class(rows: list[dict]) -> dict[str, float]:
    return _grouped_mean(rows, "hero_class")


def _ground_truth_rank_monsters(rows: list[dict]) -> list[str]:
    rates = _grouped_mean(rows, "monster")
    return [k for k, _ in sorted(rates.items(), key=lambda kv: (kv[1], kv[0]))]


def _ground_truth_unfavorable(rows: list[dict]) -> list[str]:
    rates = _grouped_mean(rows, "matchup")
    worse = [(k, v) for k, v in rates.items() if v < 0.5]
    return [k for k, _ in sorted(worse, key=lambda kv: (kv[1], kv[0]))]


def _ground_truth_conclusions(rows: list[dict]) -> dict[str, str]:
    class_rates = _grouped_mean(rows, "hero_class")
    monster_rates = _grouped_mean(rows, "monster")
    matchup_rates = _grouped_mean(rows, "matchup")
    hardest_monster = min(sorted(monster_rates.items()), key=lambda kv: kv[1])[0]
    most_balanced_class = min(sorted(class_rates.items()), key=lambda kv: abs(kv[1] - 0.5))[0]
    most_one_sided_matchup = max(sorted(matchup_rates.items()), key=lambda kv: abs(kv[1] - 0.5))[0]
    return {
        "hardest_monster": hardest_monster,
        "most_balanced_class": most_balanced_class,
        "most_one_sided_matchup": most_one_sided_matchup,
    }


def _values_close(actual: dict, expected: dict, *, rel_tol: float = 1e-3, abs_tol: float = 1e-3) -> bool:
    if set(actual.keys()) != set(expected.keys()):
        return False
    for k, exp_v in expected.items():
        act_v = actual.get(k)
        if isinstance(exp_v, (int, float)) and not isinstance(exp_v, bool):
            if act_v is None or isinstance(act_v, bool):
                return False
            try:
                if not math.isclose(float(act_v), float(exp_v), rel_tol=rel_tol, abs_tol=abs_tol):
                    return False
            except (TypeError, ValueError):
                return False
        else:
            if act_v != exp_v:
                return False
    return True


# ── AST technique gates ──────────────────────────────────────────────────

_NON_NUMPY_ATTR_RECEIVERS = {"statistics", "math"}
_COMPREHENSION_TYPES = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)


def _find_function(tree: ast.AST, fn_name: str) -> ast.FunctionDef | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == fn_name:
            return node
    return None


def _iter_non_comprehension(node: ast.AST):
    """Like ast.walk, but doesn't descend into comprehensions — a comparison
    inside `sum(1 for v in values if v > x)` is a per-element Python filter
    over scalars, not a real NumPy boolean mask."""
    stack = [node]
    while stack:
        current = stack.pop()
        if current is not node and isinstance(current, _COMPREHENSION_TYPES):
            continue
        yield current
        stack.extend(ast.iter_child_nodes(current))


def _has_real_reduction_call(fn_node: ast.AST, attr_name: str) -> bool:
    """True if `<something>.<attr_name>(...)` appears (e.g. arr.mean() or
    np.mean(arr) — both compile to the same Attribute-call shape), excluding
    a couple of non-NumPy stdlib receivers that'd match the same name."""
    for child in ast.walk(fn_node):
        if not (isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute)):
            continue
        if child.func.attr != attr_name:
            continue
        receiver = child.func.value
        if isinstance(receiver, ast.Name) and receiver.id in _NON_NUMPY_ATTR_RECEIVERS:
            continue
        return True
    return False


def _has_boolean_mask_comparison(fn_node: ast.AST) -> bool:
    compare_ops = (ast.Gt, ast.Lt, ast.GtE, ast.LtE, ast.Eq, ast.NotEq)
    for child in _iter_non_comprehension(fn_node):
        if isinstance(child, ast.Compare) and any(isinstance(op, compare_ops) for op in child.ops):
            return True
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr in {"greater", "less", "greater_equal", "less_equal", "equal", "not_equal"}
        ):
            return True
    return False


def _has_mask_combination(fn_node: ast.AST) -> bool:
    """True if two masks are combined with `&` (ast.BitAnd) or np.logical_and."""
    for child in _iter_non_comprehension(fn_node):
        if isinstance(child, ast.BinOp) and isinstance(child.op, ast.BitAnd):
            return True
        if (
            isinstance(child, ast.Call)
            and isinstance(child.func, ast.Attribute)
            and child.func.attr == "logical_and"
        ):
            return True
    return False


def _has_mask_count(fn_node: ast.AST) -> bool:
    for child in ast.walk(fn_node):
        if not isinstance(child, ast.Call):
            continue
        if isinstance(child.func, ast.Attribute) and child.func.attr in {"sum", "count_nonzero"}:
            return True
        if isinstance(child.func, ast.Name) and child.func.id == "len" and len(child.args) == 1:
            return True
    return False


def _has_2d_construction(fn_node: ast.AST) -> bool:
    for child in ast.walk(fn_node):
        if not (isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute)):
            continue
        if child.func.attr in {"column_stack", "stack", "vstack", "hstack", "dstack"}:
            return True
        if child.func.attr in {"array", "asarray"} and child.args and isinstance(child.args[0], (ast.List, ast.Tuple)):
            return True
    return False


def _has_axis_usage(fn_node: ast.AST) -> bool:
    for child in ast.walk(fn_node):
        if not isinstance(child, ast.Call):
            continue
        for kw in child.keywords:
            if kw.arg == "axis":
                return True
        if (
            isinstance(child.func, ast.Attribute)
            and child.func.attr in {"mean", "sum", "std", "median"}
            and len(child.args) >= 1
        ):
            # positional axis form: np.mean(matrix, 0) / matrix.mean(0)
            if len(child.args) >= 2 or (isinstance(child.func.value, ast.Name) and len(child.args) >= 2):
                return True
    return False


def _function_uses_attr_call(source: str, fn_name: str, attr_name: str) -> bool:
    tree = ast.parse(source)
    fn_node = _find_function(tree, fn_name)
    if fn_node is None:
        return False
    for child in ast.walk(fn_node):
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
            if child.func.attr == attr_name:
                return True
    return False


def _deep_dive_stats_gaps(source: str) -> list[str]:
    fn_node = _find_function(ast.parse(source), "deep_dive_stats")
    if fn_node is None:
        return ["deep_dive_stats function not found"]
    gaps = []
    if not _has_real_reduction_call(fn_node, "mean"):
        gaps.append("hero_win_rate must be a real NumPy mean reduction (wins.mean() or np.mean(wins))")
    if not _has_real_reduction_call(fn_node, "median"):
        gaps.append("median_rounds must be a real NumPy median (np.median(rounds))")
    if not _has_real_reduction_call(fn_node, "std"):
        gaps.append("rounds_std must be a real NumPy reduction (rounds.std() or np.std(rounds))")
    if not (_has_boolean_mask_comparison(fn_node) and _has_mask_combination(fn_node) and _has_mask_count(fn_node)):
        gaps.append("quick_hero_wins must come from a real NumPy boolean mask (hero-win comparison AND "
                    "rounds<=2 comparison, combined with `&`) counted with a NumPy op "
                    "(mask.sum(), np.count_nonzero(...), or len(arr[mask])), not a Python loop/comprehension")
    return gaps


def _matrix_summary_gaps(source: str) -> list[str]:
    fn_node = _find_function(ast.parse(source), "battle_matrix_summary")
    if fn_node is None:
        return ["battle_matrix_summary function not found"]
    gaps = []
    if not _has_2d_construction(fn_node):
        gaps.append("must build a real (N, 2) NumPy matrix (e.g. np.column_stack, np.stack, "
                    "np.vstack, or np.array of the two arrays), not two separate 1D reductions")
    if not _has_axis_usage(fn_node):
        gaps.append("must reduce the matrix with an explicit axis (e.g. matrix.mean(axis=0) or "
                    "np.mean(matrix, axis=0)), not a manual loop over rows")
    return gaps


FIXTURES_DEEP_DIVE = [
    ("primary", mission / "data" / "deep_dive_battles.json"),
    ("variant", mission / "data" / "deep_dive_battles_variant.json"),
]
FIXTURES_HISTORY = [
    ("primary", mission / "data" / "tournament_history.csv"),
    ("variant", mission / "data" / "tournament_history_variant.csv"),
]


def main() -> None:
    try:
        from task import (  # type: ignore[import]
            load_battle_arrays,
            deep_dive_stats,
            battle_matrix_summary,
            load_tournament_history,
            win_rate_by_class,
            rank_monsters,
            unfavorable_matchups,
            balance_conclusions,
            build_final_report,
        )
    except ImportError as exc:
        print(f"❌ Cannot import from task.py: {exc}")
        raise SystemExit(1)

    import numpy as np
    import pandas as pd

    # ── scaffold guard ────────────────────────────────────────────────────
    try:
        load_battle_arrays(FIXTURES_DEEP_DIVE[0][1])
    except NotImplementedError:
        print("❌ load_battle_arrays is not implemented yet — replace NotImplementedError with your code")
        raise SystemExit(1)
    except Exception:
        pass

    # ── NumPy deep-dive checks ────────────────────────────────────────────
    for fixture_name, fixture_path in FIXTURES_DEEP_DIVE:
        raw_battles = _load_deep_dive_raw(fixture_path)

        wins, rounds, gold = load_battle_arrays(fixture_path)
        for arr_name, arr in [("wins", wins), ("rounds", rounds), ("gold", gold)]:
            if not isinstance(arr, np.ndarray):
                print(f"❌ [{fixture_name}] load_battle_arrays: {arr_name} must be a NumPy ndarray, got {type(arr)}")
                raise SystemExit(1)
            if arr.shape != (len(raw_battles),):
                print(f"❌ [{fixture_name}] load_battle_arrays: {arr_name} shape {arr.shape} != "
                      f"({len(raw_battles)},)")
                raise SystemExit(1)
        expected_wins = [1 if b["winner"] == "hero" else 0 for b in raw_battles]
        if list(wins.astype(int)) != expected_wins:
            print(f"❌ [{fixture_name}] load_battle_arrays: wins array does not match winner data")
            raise SystemExit(1)
        expected_rounds = [b["rounds"] for b in raw_battles]
        if list(rounds.astype(int)) != expected_rounds:
            print(f"❌ [{fixture_name}] load_battle_arrays: rounds array does not match rounds data")
            raise SystemExit(1)
        print(f"✓ [{fixture_name}] load_battle_arrays → 3 ndarrays, shape ({len(raw_battles)},)")

        expected_stats = _ground_truth_deep_dive_stats(raw_battles)
        result = deep_dive_stats(wins, rounds)
        if not isinstance(result, dict) or not _values_close(result, expected_stats):
            print(f"❌ [{fixture_name}] deep_dive_stats: expected {expected_stats}, got {result}")
            raise SystemExit(1)
        print(f"✓ [{fixture_name}] deep_dive_stats → {result}")

        expected_matrix = _ground_truth_matrix_summary(raw_battles)
        matrix_result = battle_matrix_summary(wins, rounds)
        if not isinstance(matrix_result, dict) or not _values_close(matrix_result, expected_matrix):
            print(f"❌ [{fixture_name}] battle_matrix_summary: expected {expected_matrix}, got {matrix_result}")
            raise SystemExit(1)
        print(f"✓ [{fixture_name}] battle_matrix_summary → {matrix_result}")

    # ── Pandas tournament-history checks ─────────────────────────────────
    for fixture_name, fixture_path in FIXTURES_HISTORY:
        raw_rows = _load_history_raw(fixture_path)

        df = load_tournament_history(fixture_path)
        if not isinstance(df, pd.DataFrame):
            print(f"❌ [{fixture_name}] load_tournament_history must return a DataFrame, got {type(df)}")
            raise SystemExit(1)
        if len(df) != len(raw_rows):
            print(f"❌ [{fixture_name}] load_tournament_history: expected {len(raw_rows)} rows, got {len(df)}")
            raise SystemExit(1)
        print(f"✓ [{fixture_name}] load_tournament_history → DataFrame, {len(df)} rows")

        expected = _ground_truth_win_rate_by_class(raw_rows)
        result = win_rate_by_class(df)
        if not isinstance(result, dict) or not _values_close(result, expected):
            print(f"❌ [{fixture_name}] win_rate_by_class: expected {expected}, got {result}")
            raise SystemExit(1)
        print(f"✓ [{fixture_name}] win_rate_by_class → {result}")

        expected_ranking = _ground_truth_rank_monsters(raw_rows)
        ranking_result = rank_monsters(df)
        if list(ranking_result) != expected_ranking:
            print(f"❌ [{fixture_name}] rank_monsters: expected {expected_ranking}, got {ranking_result}")
            raise SystemExit(1)
        print(f"✓ [{fixture_name}] rank_monsters → {ranking_result}")

        expected_unfav = _ground_truth_unfavorable(raw_rows)
        unfav_result = unfavorable_matchups(df)
        if list(unfav_result) != expected_unfav:
            print(f"❌ [{fixture_name}] unfavorable_matchups: expected {expected_unfav}, got {unfav_result}")
            raise SystemExit(1)
        print(f"✓ [{fixture_name}] unfavorable_matchups → {unfav_result}")

        expected_conclusions = _ground_truth_conclusions(raw_rows)
        conclusions_result = balance_conclusions(df)
        if not isinstance(conclusions_result, dict) or not _values_close(conclusions_result, expected_conclusions):
            print(f"❌ [{fixture_name}] balance_conclusions: expected {expected_conclusions}, got {conclusions_result}")
            raise SystemExit(1)
        print(f"✓ [{fixture_name}] balance_conclusions → {conclusions_result}")

    # ── Final synthesis checks (paired primary/variant scenarios) ────────
    scenarios = [
        ("primary", FIXTURES_DEEP_DIVE[0][1], FIXTURES_HISTORY[0][1]),
        ("variant", FIXTURES_DEEP_DIVE[1][1], FIXTURES_HISTORY[1][1]),
    ]
    for scenario_name, deep_dive_path, history_path in scenarios:
        raw_battles = _load_deep_dive_raw(deep_dive_path)
        raw_rows = _load_history_raw(history_path)
        expected_report = {
            "deep_dive": _ground_truth_deep_dive_stats(raw_battles),
            "matrix_summary": _ground_truth_matrix_summary(raw_battles),
            "win_rate_by_class": _ground_truth_win_rate_by_class(raw_rows),
            "monster_ranking": _ground_truth_rank_monsters(raw_rows),
            "unfavorable_matchups": _ground_truth_unfavorable(raw_rows),
            "conclusions": _ground_truth_conclusions(raw_rows),
        }
        report = build_final_report(deep_dive_path, history_path)
        if not isinstance(report, dict):
            print(f"❌ [{scenario_name}] build_final_report must return a dict, got {type(report)}")
            raise SystemExit(1)
        for key in expected_report:
            if key not in report:
                print(f"❌ [{scenario_name}] build_final_report: missing key '{key}'")
                raise SystemExit(1)
            expected_value = expected_report[key]
            actual_value = report[key]
            if isinstance(expected_value, dict):
                if not isinstance(actual_value, dict) or not _values_close(actual_value, expected_value):
                    print(f"❌ [{scenario_name}] build_final_report['{key}']: "
                          f"expected {expected_value}, got {actual_value}")
                    raise SystemExit(1)
            else:
                if list(actual_value) != list(expected_value):
                    print(f"❌ [{scenario_name}] build_final_report['{key}']: "
                          f"expected {expected_value}, got {actual_value}")
                    raise SystemExit(1)
        print(f"✓ [{scenario_name}] build_final_report matches its own input fixtures")

    # ── NumPy technique gates ─────────────────────────────────────────────
    src = (mission / "task.py").read_text()

    _percentile_used = False
    _original_percentile, _original_quantile = np.percentile, np.quantile

    def _percentile_spy(*args, **kwargs):
        nonlocal _percentile_used
        _percentile_used = True
        return _original_percentile(*args, **kwargs)

    def _quantile_spy(*args, **kwargs):
        nonlocal _percentile_used
        _percentile_used = True
        return _original_quantile(*args, **kwargs)

    np.percentile, np.quantile = _percentile_spy, _quantile_spy
    try:
        wins, rounds, _gold = load_battle_arrays(FIXTURES_DEEP_DIVE[0][1])
        deep_dive_stats(wins, rounds)
    finally:
        np.percentile, np.quantile = _original_percentile, _original_quantile

    gaps = _deep_dive_stats_gaps(src)
    if not _percentile_used:
        gaps.append("rounds_p90 must call np.percentile or np.quantile, not a manual percentile formula")
    if gaps:
        print("❌ deep_dive_stats does not use NumPy for all required recall objectives:")
        for gap in gaps:
            print(f"   - {gap}")
        raise SystemExit(1)
    print("✓ deep_dive_stats uses real NumPy reductions, percentile/quantile, and boolean-mask work")

    matrix_gaps = _matrix_summary_gaps(src)
    if matrix_gaps:
        print("❌ battle_matrix_summary does not use a real 2D NumPy matrix + axis aggregation:")
        for gap in matrix_gaps:
            print(f"   - {gap}")
        raise SystemExit(1)
    print("✓ battle_matrix_summary builds a real 2D matrix and reduces it along axis=0")

    # ── Pandas technique gates: groupby is the learning objective ────────
    for fn_name in ("win_rate_by_class", "rank_monsters", "unfavorable_matchups"):
        if not _function_uses_attr_call(src, fn_name, "groupby"):
            print(f"❌ {fn_name} must use pandas' groupby — a per-group Python loop "
                  f"(e.g. over .unique()) produces the same numbers but skips the "
                  f"learning objective of this task")
            raise SystemExit(1)
    print("✓ win_rate_by_class, rank_monsters, and unfavorable_matchups all use pandas groupby")

    update_progress()
    print("\n✅ Final Analytics Epilogue complete! Is the game balanced? You've got the data to say.")


if __name__ == "__main__":
    main()
