import ast
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parents[2]
PROGRESS_FILE = REPO_ROOT / ".progress"
MISSION_ID = "21_from_combat_log_to_dataframe"


def _update_progress(status: str) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text())
    data.setdefault("missions", {})[MISSION_ID] = status
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def main() -> None:
    import pandas as pd
    import task

    # --- Inspect habit: encourage looking before calculating, without
    # parsing fragile print() output. Parsing the AST (not just scanning
    # text) means the instructional comment's own wording ("df.head()...")
    # can't accidentally satisfy this — only real code counts.
    task_src = (Path(__file__).parent / "task.py").read_text()
    attrs_used = {n.attr for n in ast.walk(ast.parse(task_src)) if isinstance(n, ast.Attribute)}
    inspect_attrs = {"head", "shape", "columns", "dtypes", "info"}
    found = inspect_attrs & attrs_used
    assert len(found) >= 3, (
        "Before calculating anything, look at what you loaded — call at least "
        "a few of df.head(), df.shape, df.columns, df.dtypes, df.info() as real "
        f"code, not just in a comment. Found {len(found)}/5: {sorted(found)}"
    )

    # --- Load ---
    assert isinstance(task.df, pd.DataFrame), (
        f"df should be a DataFrame, got {type(task.df).__name__} — did you call pd.read_csv()?"
    )
    assert task.df.shape == (9, 3), f"df should have 9 rows and 3 columns, got {task.df.shape}"
    assert list(task.df.columns) == ["round", "hero_hp", "boss_hp"], (
        f"Columns should be ['round', 'hero_hp', 'boss_hp'], got {list(task.df.columns)}"
    )

    # --- Inspect: dtype checked by meaning, not by exact platform representation ---
    for col in ("round", "hero_hp", "boss_hp"):
        assert pd.api.types.is_numeric_dtype(task.df[col]), (
            f"Column '{col}' should hold numeric values, got dtype {task.df[col].dtype}"
        )

    assert task.summary is not None, "summary is still None — did you assign df.describe()?"
    for stat in ("mean", "std", "min", "max"):
        assert stat in task.summary.index, (
            f"summary should be the result of df.describe() — missing the '{stat}' row"
        )
    assert "hero_hp" in task.summary.columns, (
        "summary should describe the numeric columns, including 'hero_hp'"
    )

    # --- The three questions ---
    expected_avg = float(task.df["hero_hp"].mean())
    assert task.avg_hero_hp is not None, "avg_hero_hp is still None"
    assert abs(task.avg_hero_hp - expected_avg) < 0.01, (
        f"avg_hero_hp should be {expected_avg:.2f}, got {task.avg_hero_hp}"
    )

    expected_min = int(task.df["hero_hp"].min())
    assert task.min_hero_hp is not None, "min_hero_hp is still None"
    assert int(task.min_hero_hp) == expected_min, (
        f"min_hero_hp should be {expected_min}, got {task.min_hero_hp}"
    )

    assert task.final_round is not None, "final_round is still None"
    assert int(task.final_round) == 9, f"final_round should be 9, got {task.final_round}"

    # --- Notice: missing data ---
    assert isinstance(task.missing_hp, pd.Series) and task.missing_hp.dtype == bool, (
        f"missing_hp should be a boolean Series (messy_df['hero_hp'].isna()), "
        f"got {type(task.missing_hp).__name__}"
    )
    assert int(task.missing_hp.sum()) == 1, (
        f"messy_log.csv has exactly one missing hero_hp value; "
        f"missing_hp should have exactly one True, got {int(task.missing_hp.sum())}"
    )
    assert task.missing_hp_count == 1, (
        f"missing_hp_count should be 1, got {task.missing_hp_count}"
    )

    # --- Decide: clean_df must actually be cleaned, not just aliased ---
    assert isinstance(task.clean_df, pd.DataFrame), (
        f"clean_df should be a DataFrame, got {type(task.clean_df).__name__}"
    )
    assert len(task.clean_df) == len(task.messy_df) - 1, (
        f"clean_df should have one fewer row than messy_df (the missing-HP round "
        f"dropped) — messy_df has {len(task.messy_df)} rows, clean_df has {len(task.clean_df)}"
    )
    assert task.clean_df["hero_hp"].isna().sum() == 0, (
        "clean_df still contains a missing hero_hp value — did dropna() actually run, "
        "or was clean_df just set equal to messy_df?"
    )

    _update_progress("complete")
    print("✅ Mission 21 complete: From Combat Log to DataFrame")
    print("   Next mission: level_1_python_basics/missions/22_filter_group_rank/README.md")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        _update_progress("in_progress")
        print(f"❌ Not quite: {e}")
        raise SystemExit(1)
    except Exception as e:
        _update_progress("in_progress")
        print(f"❌ Error: {e}")
        raise SystemExit(1)
