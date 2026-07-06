"""check.py — Project 01: Async Quest Aggregator"""

import ast
import asyncio
import json
import sys
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PROGRESS_FILE = Path(__file__).parents[3] / "level_7_concurrency_and_background_work" / ".progress"

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


def _uses_gather_in_fn(source: str, fn_name: str) -> bool:
    """Return True if asyncio.gather is called inside fn_name."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
            continue
        if node.name != fn_name:
            continue
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                func = child.func
                if isinstance(func, ast.Attribute) and func.attr == "gather":
                    return True
    return False


def main() -> None:
    # ── 1. Import ─────────────────────────────────────────────────────────────
    try:
        from task import AggregateResult, Quest, aggregate_all_quests
    except ImportError as exc:
        print(f"❌ Cannot import from task.py: {exc}")
        raise SystemExit(1)

    # ── 2. AggregateResult has correct fields ─────────────────────────────────
    import dataclasses
    if not dataclasses.is_dataclass(AggregateResult):
        print("❌ AggregateResult must be a @dataclass")
        raise SystemExit(1)
    fields = {f.name for f in dataclasses.fields(AggregateResult)}
    for expected in ("quests", "failed_sources", "elapsed"):
        if expected not in fields:
            print(f"❌ AggregateResult must have field '{expected}'")
            raise SystemExit(1)
    print("✓ AggregateResult dataclass has quests, failed_sources, elapsed")

    # ── 3. Scaffold guard ─────────────────────────────────────────────────────
    try:
        asyncio.run(aggregate_all_quests(5.0))
    except NotImplementedError:
        print("❌ task.py is not implemented yet — replace NotImplementedError with real code")
        raise SystemExit(1)
    except Exception:
        pass

    # ── 4. Generous timeout (5.0s): all 3 sources succeed ────────────────────
    # Sources: guild=0.1s, village=0.05s, royal=0.2s — all well under 5s
    result = asyncio.run(aggregate_all_quests(5.0))
    if not isinstance(result, AggregateResult):
        print(f"❌ aggregate_all_quests() must return AggregateResult, got {type(result)}")
        raise SystemExit(1)
    if len(result.failed_sources) != 0:
        print(f"❌ With 5.0s timeout, no sources should fail. Got: {result.failed_sources}")
        raise SystemExit(1)
    if len(result.quests) < 3:
        print(f"❌ With 5.0s timeout, expected ≥3 quests total, got {len(result.quests)}")
        raise SystemExit(1)
    print(f"✓ Generous timeout: {len(result.quests)} quests, 0 failures")

    # ── 5. Tight timeout (0.15s): only royal (0.2s) times out ────────────────
    # guild=0.1s < 0.15s → succeeds; royal=0.2s > 0.15s → fails
    result_tight = asyncio.run(aggregate_all_quests(0.15))
    if "royal" not in result_tight.failed_sources:
        print(
            f"❌ With 0.15s timeout, 'royal' (0.2s) should be in failed_sources. "
            f"Got: {result_tight.failed_sources}"
        )
        raise SystemExit(1)
    if "guild" in result_tight.failed_sources:
        print(
            f"❌ With 0.15s timeout, 'guild' (0.1s) should succeed, not fail. "
            f"Got: {result_tight.failed_sources}"
        )
        raise SystemExit(1)
    guild_quests = [q for q in result_tight.quests if q.source == "guild"]
    if len(guild_quests) == 0:
        print("❌ 'guild' (0.1s) should have quests with 0.15s timeout")
        raise SystemExit(1)
    print(
        f"✓ Tight timeout: {result_tight.failed_sources} failed, "
        f"{len(result_tight.quests)} quest(s) from remaining sources"
    )

    # ── 6. Timing proof: 5.0s timeout completes well under 0.4s ─────────────
    # Sequential would be 0.1+0.05+0.2=0.35s; concurrent should be ~0.2s
    t0 = time.monotonic()
    asyncio.run(aggregate_all_quests(5.0))
    elapsed = time.monotonic() - t0
    if elapsed > 0.4:
        print(f"❌ aggregate_all_quests(5.0) took {elapsed:.3f}s — must be concurrent (<0.4s)")
        print("   Sequential sum: 0.1+0.05+0.2=0.35s; concurrent should be ~0.2s")
        raise SystemExit(1)
    print(f"✓ Timing: completed in {elapsed:.3f}s (concurrent, not sequential)")

    # ── 7. AST: asyncio.gather used inside aggregate_all_quests ──────────────
    source = (PROJECT_DIR / "task.py").read_text(encoding="utf-8")
    if not _uses_gather_in_fn(source, "aggregate_all_quests"):
        print("❌ aggregate_all_quests must use asyncio.gather() — not sequential awaits")
        raise SystemExit(1)
    print("✓ asyncio.gather() used inside aggregate_all_quests")

    # ── Done ──────────────────────────────────────────────────────────────────
    update_progress("01_async_quest_aggregator")
    print()
    print("✅ Project 01 complete: Async Quest Aggregator works!")
    print()
    print("   asyncio.gather + wait_for = concurrent fetches with per-source timeout.")
    print("   One slow source can't hold up the others.")


if __name__ == "__main__":
    main()
