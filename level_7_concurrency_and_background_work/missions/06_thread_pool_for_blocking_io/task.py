"""Mission 06: Thread Pool for Blocking I/O.

Goal:  Use ThreadPoolExecutor to export session reports concurrently.
       I/O-bound work (reading files, writing files) benefits from threads.
Check: uv run python check.py
"""
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def export_one_session(session_id: str, sessions_dir: Path, output_dir: Path) -> Path:
    """Read one session JSON, write a Markdown report, return output path."""
    import json
    data = json.loads((sessions_dir / f"{session_id}.json").read_text())
    outcome = "Victory" if data["winner"] == "hero" else "Defeat"
    md = (
        f"## Battle Report — {session_id[:8]}\n\n"
        f"**Hero:** {data['hero_name']}  \n"
        f"**Monster:** {data['monster_name']}  \n"
        f"**Outcome:** {outcome}  \n"
        f"**Rounds:** {data['rounds']}  \n"
        f"**Gold earned:** {data['gold_earned']}\n"
    )
    out = output_dir / f"{session_id}.md"
    out.write_text(md)
    return out


def export_sessions_sequential(
    session_ids: list[str], sessions_dir: Path, output_dir: Path
) -> list[Path]:
    """Export sessions one by one (sequential baseline)."""
    return [export_one_session(sid, sessions_dir, output_dir) for sid in session_ids]


def export_sessions_parallel(
    session_ids: list[str], sessions_dir: Path, output_dir: Path, workers: int = 4
) -> list[Path]:
    """TODO: Export sessions concurrently using ThreadPoolExecutor.
    Use pool.submit() or pool.map() to call export_one_session for each session_id.
    Return list of output paths.
    """
    raise NotImplementedError
