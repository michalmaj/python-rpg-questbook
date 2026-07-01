"""Check: Mission 06 — session reports."""

import importlib.util
import json
import tempfile
from datetime import datetime
from pathlib import Path

task_path = Path(__file__).parent / "task.py"

spec = importlib.util.spec_from_file_location("task06", task_path)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # type: ignore[union-attr]

SessionSummary = mod.SessionSummary
generate_json_report = getattr(mod, "generate_json_report", None)
generate_md_report = getattr(mod, "generate_md_report", None)
generate_reports = getattr(mod, "generate_reports", None)

for fn_name in ("generate_json_report", "generate_md_report", "generate_reports"):
    if getattr(mod, fn_name, None) is None:
        print(f"❌ {fn_name}() not found in task.py")
        raise SystemExit(1)

# ── sample session ------------------------------------------------------------

session = SessionSummary(
    started_at=datetime(2026, 7, 1, 15, 30),
    hero_name="Ada",
    hero_class="warrior",
    battles=5,
    wins=3,
    losses=2,
    gold_earned=70,
    final_hp=96,
    max_hp=120,
)

# ── to_markdown() implemented -------------------------------------------------

try:
    md = session.to_markdown()
except NotImplementedError:
    print("❌ SessionSummary.to_markdown() not yet implemented")
    raise SystemExit(1)

for expected in ("Ada", "warrior", "3", "2", "70"):
    if expected not in md:
        print(f"❌ to_markdown(): expected '{expected}' in output")
        raise SystemExit(1)
print("✓ to_markdown() includes name, class, wins, losses, gold")

if "#" not in md:
    print("❌ to_markdown(): no Markdown heading (# ...) found")
    raise SystemExit(1)
print("✓ to_markdown() contains a Markdown heading")

# ── generate_json_report ─────────────────────────────────────────────────────

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "sub" / "session.json"
    try:
        generate_json_report(session, path)
    except NotImplementedError:
        print("❌ generate_json_report() not yet implemented")
        raise SystemExit(1)

    if not path.exists():
        print("❌ generate_json_report() did not create the file")
        raise SystemExit(1)

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        print(f"❌ generate_json_report() wrote invalid JSON: {e}")
        raise SystemExit(1)

    if data.get("hero_name") != "Ada":
        print("❌ JSON report missing or wrong hero_name")
        raise SystemExit(1)
    if data.get("wins") != 3:
        print("❌ JSON report missing or wrong wins")
        raise SystemExit(1)
    print("✓ generate_json_report() writes valid JSON with correct data")

# ── generate_md_report ────────────────────────────────────────────────────────

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "sub" / "session.md"
    try:
        generate_md_report(session, path)
    except NotImplementedError:
        print("❌ generate_md_report() not yet implemented")
        raise SystemExit(1)

    if not path.exists():
        print("❌ generate_md_report() did not create the file")
        raise SystemExit(1)

    content = path.read_text()
    if "Ada" not in content:
        print("❌ Markdown report missing hero name")
        raise SystemExit(1)
    print("✓ generate_md_report() writes Markdown with hero name")

# ── generate_reports — filenames and return value ────────────────────────────

with tempfile.TemporaryDirectory() as tmp:
    reports_dir = Path(tmp)
    try:
        json_path, md_path = generate_reports(session, reports_dir)
    except NotImplementedError:
        print("❌ generate_reports() not yet implemented")
        raise SystemExit(1)

    if not json_path.exists():
        print(f"❌ generate_reports() did not create {json_path}")
        raise SystemExit(1)
    if not md_path.exists():
        print(f"❌ generate_reports() did not create {md_path}")
        raise SystemExit(1)
    print("✓ generate_reports() creates both files")

    # check timestamped filenames
    if "2026-07-01_1530" not in json_path.name:
        print(f"❌ JSON filename should contain '2026-07-01_1530', got '{json_path.name}'")
        raise SystemExit(1)
    if "2026-07-01_1530" not in md_path.name:
        print(f"❌ MD filename should contain '2026-07-01_1530', got '{md_path.name}'")
        raise SystemExit(1)
    print("✓ generate_reports() uses timestamped filenames")

    if json_path.suffix != ".json":
        print(f"❌ Expected .json suffix, got '{json_path.suffix}'")
        raise SystemExit(1)
    if md_path.suffix != ".md":
        print(f"❌ Expected .md suffix, got '{md_path.suffix}'")
        raise SystemExit(1)
    print("✓ generate_reports() uses .json and .md suffixes")

print("\n✅ Mission 06 complete!")
