"""Check: Mission 06 — Thread Pool for Blocking I/O."""
import json
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
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


try:
    from task import export_sessions_parallel, export_sessions_sequential  # type: ignore
except ImportError as exc:
    print(f"❌ Cannot import from task.py: {exc}")
    raise SystemExit(1)

sessions_dir = Path(__file__).parent / "data" / "sessions"
session_ids = [p.stem for p in sessions_dir.glob("*.json")]
if len(session_ids) < 5:
    print(f"❌ Expected 5 session files in data/sessions/, found {len(session_ids)}")
    raise SystemExit(1)

with tempfile.TemporaryDirectory() as tmp:
    out_dir = Path(tmp)

    # sequential baseline
    t0 = time.perf_counter()
    seq_results = export_sessions_sequential(session_ids, sessions_dir, out_dir)
    seq_time = time.perf_counter() - t0
    if len(seq_results) != len(session_ids):
        print(f"❌ Sequential export returned {len(seq_results)} paths, expected {len(session_ids)}")
        raise SystemExit(1)
    print(f"✓ export_sessions_sequential: {seq_time:.3f}s for {len(session_ids)} sessions")

    # parallel
    try:
        par_results = export_sessions_parallel(session_ids, sessions_dir, out_dir, workers=4)
    except NotImplementedError:
        print("❌ export_sessions_parallel not implemented")
        raise SystemExit(1)
    if len(par_results) != len(session_ids):
        print(f"❌ Parallel export returned {len(par_results)} paths, expected {len(session_ids)}")
        raise SystemExit(1)
    for path in par_results:
        if not Path(path).exists():
            print(f"❌ Output file not created: {path}")
            raise SystemExit(1)
    print(f"✓ export_sessions_parallel: {len(par_results)} files exported")

    # verify markdown content
    sample = Path(par_results[0]).read_text()
    if "## Battle Report" not in sample:
        print("❌ Exported Markdown missing '## Battle Report' header")
        raise SystemExit(1)
    print("✓ Exported Markdown contains '## Battle Report'")

# verify ThreadPoolExecutor is actually used inside export_sessions_parallel
import ast

src = (Path(__file__).parent / "task.py").read_text()
tree = ast.parse(src)
parallel_func = next(
    (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "export_sessions_parallel"),
    None,
)
if parallel_func is None:
    print("❌ export_sessions_parallel not found in task.py")
    raise SystemExit(1)

func_src = ast.get_source_segment(src, parallel_func) or ""
if "ThreadPoolExecutor" not in func_src:
    print("❌ export_sessions_parallel must use ThreadPoolExecutor (found import but not used in the function body)")
    raise SystemExit(1)
print("✓ ThreadPoolExecutor used inside export_sessions_parallel")

update_progress("06_thread_pool_for_blocking_io")
print("\n✅ Mission 06 complete! ThreadPoolExecutor for I/O-bound work.")
