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

# ── Behavioral proof: the pool must actually be used to dispatch the work ────
#
# The functional test above would also pass for a fake that creates a
# ThreadPoolExecutor, never calls submit()/map() on it, and silently falls
# back to export_sessions_sequential(). Replace ThreadPoolExecutor with a
# recording stand-in that executes work synchronously (so results stay
# correct) but records every independent item handed to submit()/map().

import task as _task_mod


class _RecordingFuture:
    def __init__(self, value=None, exc=None):
        self._value = value
        self._exc = exc

    def result(self, timeout=None):
        if self._exc is not None:
            raise self._exc
        return self._value


class _RecordingThreadPoolExecutor:
    """Drop-in stand-in for ThreadPoolExecutor: runs work inline, records items."""

    instances: list = []

    def __init__(self, max_workers=None, *args, **kwargs):
        self.max_workers = max_workers
        self.submitted_items: list = []
        _RecordingThreadPoolExecutor.instances.append(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def submit(self, fn, *args, **kwargs):
        self.submitted_items.append((fn, args, kwargs))
        try:
            return _RecordingFuture(value=fn(*args, **kwargs))
        except Exception as exc:  # noqa: BLE001 - mirrors real Future semantics
            return _RecordingFuture(exc=exc)

    def map(self, fn, *iterables):
        results = []
        for call_args in zip(*iterables):
            self.submitted_items.append((fn, call_args, {}))
            results.append(fn(*call_args))
        return iter(results)

    def shutdown(self, wait=True, *args, **kwargs):
        pass


_RecordingThreadPoolExecutor.instances.clear()
_original_executor = _task_mod.ThreadPoolExecutor
_task_mod.ThreadPoolExecutor = _RecordingThreadPoolExecutor

try:
    with tempfile.TemporaryDirectory() as tmp2:
        out_dir2 = Path(tmp2)
        rec_results = export_sessions_parallel(session_ids, sessions_dir, out_dir2, workers=4)

        total_items = sum(len(inst.submitted_items) for inst in _RecordingThreadPoolExecutor.instances)
        if total_items == 0:
            print("❌ ThreadPoolExecutor was created but never used (no submit()/map() calls).")
            print("   Creating the pool isn't enough — you must hand it the work.")
            raise SystemExit(1)
        if total_items < 2:
            print(f"❌ Only {total_items} independent work item was submitted to the pool.")
            print("   Each session should be its own independent unit of work, not one bundled call.")
            raise SystemExit(1)
        if len(rec_results) != len(session_ids):
            print(f"❌ export_sessions_parallel returned {len(rec_results)} paths, expected {len(session_ids)}")
            raise SystemExit(1)
        for path in rec_results:
            if not Path(path).exists():
                print(f"❌ Output file not created: {path}")
                raise SystemExit(1)
        print(f"✓ ThreadPoolExecutor actually used — {total_items} independent work items submitted, "
              f"all {len(session_ids)} sessions exported correctly")
finally:
    _task_mod.ThreadPoolExecutor = _original_executor

update_progress("06_thread_pool_for_blocking_io")
print("\n✅ Mission 06 complete! ThreadPoolExecutor for I/O-bound work.")
