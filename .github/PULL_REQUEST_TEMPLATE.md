## What does this PR do?

<!-- One sentence. "Add Mission X", "Fix check.py gate Y", "Refactor Z" -->

## Type

- [ ] New mission / project
- [ ] Bug fix (broken check.py, wrong scaffold, bad link)
- [ ] Content fix (README, task.py clarity, docstring)
- [ ] Tooling (author_check, course_status, CI)
- [ ] Other

## Checklist

- [ ] `uv run python tools/author_check.py` — 0 errors
- [ ] New missions have: `README.md`, `task.py` (with `raise NotImplementedError`), `check.py` (with `raise SystemExit(1)` on failure)
- [ ] New projects have: `README.md`, `check.py`
- [ ] check.py uses `sys.executable`, not `"uv", "run", "python"` in subprocess calls
- [ ] No solution code leaked into `task.py`
- [ ] README commands run from repo root
- [ ] COURSE_MAP.md updated if structure changed
