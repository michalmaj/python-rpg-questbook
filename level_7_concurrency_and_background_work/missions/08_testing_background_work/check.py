"""Check: Mission 08 — Testing Background Work.

Structural checks confirm SyncWorker is used, no sleep()/threading.Event, and
at least 6 test functions exist. The real proof of competence is behavioral:
the student's test suite must pass against the correct code, then FAIL
against each of six independent, single-behavior mutants — one per required
behavior from the README (new job pending, submit completes, exception
stores error, result stored, two jobs independent, unknown job returns
None). A suite of tests that make real calls but assert nothing meaningful
(`assert True`) kills none of these mutants.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
mission = Path(__file__).parent
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
    for d in mission.rglob("__pycache__"):
        shutil.rmtree(d, ignore_errors=True)


def _run_pytest() -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(mission)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    _clear_pycache()
    try:
        return subprocess.run(
            [sys.executable, "-m", "pytest", "task/tests/test_background.py", "-q", "--tb=line"],
            capture_output=True, text=True, cwd=str(mission), env=env,
        )
    finally:
        _clear_pycache()


# ── test file exists ──────────────────────────────────────────────────────────

test_file = mission / "task" / "tests" / "test_background.py"
if not test_file.exists():
    print("❌ task/tests/test_background.py not found")
    raise SystemExit(1)

src = test_file.read_text()

# ── SyncWorker used ───────────────────────────────────────────────────────────

if "SyncWorker" not in src:
    print("❌ SyncWorker not imported/used in test_background.py")
    raise SystemExit(1)
print("✓ SyncWorker used in tests")

# ── no time.sleep / threading.Event ──────────────────────────────────────────

code_lines = [ln for ln in src.splitlines() if not ln.lstrip().startswith("#")]
code_src = "\n".join(code_lines)
if "time.sleep" in code_src:
    print("❌ time.sleep() found — use SyncWorker for deterministic tests")
    raise SystemExit(1)
print("✓ No time.sleep() — deterministic tests")

# ── at least 6 test functions ─────────────────────────────────────────────────

test_fn_count = sum(
    1 for ln in src.splitlines()
    if ln.lstrip().startswith("def test_") and not ln.lstrip().startswith("#")
)
if test_fn_count < 6:
    print(f"❌ Found {test_fn_count} test functions — write at least 6")
    raise SystemExit(1)
print(f"✓ {test_fn_count} test functions found")

# ── Gate 1: the suite must pass against the correct code ─────────────────────

result = _run_pytest()
if result.returncode != 0:
    print("❌ pytest fails against the correct code:")
    print(result.stdout[-2000:])
    print(result.stderr[-500:])
    raise SystemExit(1)
print("✓ All background tests pass against the correct code")

# ── Gate 2: the suite must FAIL against each single-behavior mutant ──────────
#
# One mutant per behavior the README's test table asks for. Each mutates
# task/jobs.py's InMemoryJobRepository or task/workers.py's SyncWorker — the
# two components the mission's own tests exercise directly (not through
# BackgroundWorker, which the mission explicitly says not to use in tests).

JOBS_FILE = mission / "task" / "jobs.py"
WORKERS_FILE = mission / "task" / "workers.py"

for path in (JOBS_FILE, WORKERS_FILE):
    if not path.exists():
        print(f"❌ {path.relative_to(mission)} not found")
        raise SystemExit(1)

originals = {p: p.read_text() for p in (JOBS_FILE, WORKERS_FILE)}

_SYNC_WORKER_BLOCK = (
    '    """Runs jobs inline (no threading). Use in tests for determinism."""\n'
    "    def __init__(self, repo: JobRepository) -> None:\n"
    "        self._repo = repo\n"
    "\n"
    "    def submit(self, job_id: str, fn: Callable[[], Any]) -> None:\n"
    "        self._repo.set_status(job_id, JobStatus.running)\n"
    "        try:\n"
    "            result = fn()\n"
    "            self._repo.set_result(job_id, result)\n"
    "            self._repo.set_status(job_id, JobStatus.completed)\n"
    "        except Exception as exc:\n"
    "            self._repo.set_error(job_id, str(exc))\n"
    "            self._repo.set_status(job_id, JobStatus.failed)"
)

MUTANTS: list[tuple[str, Path, str, str]] = [
    (
        "a new job starts as something other than pending",
        JOBS_FILE,
        "    def create(self, job_id: str) -> Job:\n"
        "        job = Job(id=job_id, status=JobStatus.pending)\n"
        "        with self._lock:\n"
        "            self._jobs[job_id] = job",
        "    def create(self, job_id: str) -> Job:\n"
        "        job = Job(id=job_id, status=JobStatus.completed)\n"
        "        with self._lock:\n"
        "            self._jobs[job_id] = job",
    ),
    (
        "SyncWorker.submit() never marks the job completed (stuck on 'running')",
        WORKERS_FILE,
        _SYNC_WORKER_BLOCK,
        _SYNC_WORKER_BLOCK.replace(
            "            self._repo.set_result(job_id, result)\n"
            "            self._repo.set_status(job_id, JobStatus.completed)\n",
            "            self._repo.set_result(job_id, result)\n",
        ),
    ),
    (
        "a raised exception is swallowed — job looks completed instead of failed",
        WORKERS_FILE,
        _SYNC_WORKER_BLOCK,
        _SYNC_WORKER_BLOCK.replace(
            "        except Exception as exc:\n"
            "            self._repo.set_error(job_id, str(exc))\n"
            "            self._repo.set_status(job_id, JobStatus.failed)",
            "        except Exception:\n"
            "            self._repo.set_status(job_id, JobStatus.completed)",
        ),
    ),
    (
        "the job completes but its result is never stored",
        WORKERS_FILE,
        _SYNC_WORKER_BLOCK,
        _SYNC_WORKER_BLOCK.replace(
            "            self._repo.set_result(job_id, result)\n",
            "",
        ),
    ),
    (
        "two independent jobs end up sharing the same result",
        JOBS_FILE,
        "    def set_result(self, job_id: str, result: dict) -> None:\n"
        "        with self._lock:\n"
        "            if job := self._jobs.get(job_id):\n"
        "                job.result = result",
        "    def set_result(self, job_id: str, result: dict) -> None:\n"
        "        with self._lock:\n"
        "            for job in self._jobs.values():\n"
        "                job.result = result",
    ),
    (
        "an unknown job_id returns a fabricated job instead of None",
        JOBS_FILE,
        "    def get(self, job_id: str) -> Job | None:\n"
        "        with self._lock:\n"
        "            return self._jobs.get(job_id)",
        "    def get(self, job_id: str) -> Job | None:\n"
        "        with self._lock:\n"
        "            return self._jobs.get(job_id) or Job(id=job_id, status=JobStatus.completed, result={})",
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
                  "behavior breaks — check the actual status/result/error, not just that calls don't crash.")
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

update_progress("08_testing_background_work")
print("\n✅ Mission 08 complete! Deterministic tests for background work.")
