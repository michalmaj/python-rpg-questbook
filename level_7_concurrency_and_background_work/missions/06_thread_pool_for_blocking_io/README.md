# Mission 06: Thread Pool for Blocking I/O

## Goal

Use `ThreadPoolExecutor` to export session reports concurrently. I/O-bound work (reading files, writing files) benefits from threads because threads can wait for I/O operations independently.

## Given

- `export_one_session()` — Reads one session JSON file and writes a Markdown battle report
- `export_sessions_sequential()` — Exports all sessions one by one (your baseline)

Both of these functions are already implemented in `task.py`.

## Your Task

Implement `export_sessions_parallel()` using `ThreadPoolExecutor`. This function should:

1. Create a thread pool with the specified number of workers
2. Submit `export_one_session()` tasks to the pool for each session ID
3. Collect and return the output paths

## Hint

You can use either `pool.map()` or `pool.submit()`:

**Option 1: Using `pool.map()`**
```python
with ThreadPoolExecutor(max_workers=workers) as pool:
    return list(pool.map(
        lambda sid: export_one_session(sid, sessions_dir, output_dir),
        session_ids
    ))
```

**Option 2: Using `pool.submit()`**
```python
with ThreadPoolExecutor(max_workers=workers) as pool:
    futures = [pool.submit(export_one_session, sid, sessions_dir, output_dir)
               for sid in session_ids]
    return [f.result() for f in futures]
```

## Key Insight

- **Threads help I/O-bound work**: while one thread waits for a file read or write, another thread can start its own I/O. This overlaps I/O operations.
- **Threads don't help CPU-bound work**: multiple threads on one CPU core don't run in parallel because the GIL (Global Interpreter Lock) prevents true parallelism. Use `ProcessPoolExecutor` for CPU-bound tasks (Mission 07).

## How to Check

```bash
cd level_7_concurrency_and_background_work/missions/06_thread_pool_for_blocking_io
uv run python check.py
```

The checker will:
1. Verify both sequential and parallel exports work
2. Confirm all output files are created
3. Validate Markdown content
4. Confirm `ThreadPoolExecutor` is used in your code

## What's in `data/sessions/`

Five pre-made battle session JSON files (session-001.json through session-005.json), each containing:
- `hero_name`, `monster_name`, `winner`, `rounds`, `gold_earned`

Your function reads these and exports them as Markdown reports.
