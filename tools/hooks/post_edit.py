#!/usr/bin/env python3
"""Claude Code PostToolUse hook (Edit|Write|MultiEdit).

Validates ONLY the markdown file that was just edited (≈0.2 s). On errors it exits 2 and
prints them to stderr, which Claude Code feeds back to the agent so it fixes them
immediately. Non-content files are ignored.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WATCHED = ("Python/", "Django DRF/", "Django ORM/", "Django ORM Short/", "django/", "React/", "prompts/")

try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)
path = (payload.get("tool_input") or {}).get("file_path") or (payload.get("tool_response") or {}).get("filePath")
if not path or not path.endswith(".md"):
    sys.exit(0)
try:
    rel = Path(path).resolve().relative_to(ROOT).as_posix()
except ValueError:
    sys.exit(0)
if not rel.startswith(WATCHED):
    sys.exit(0)

res = subprocess.run([sys.executable, str(ROOT / "tools" / "validate.py"), "--file", rel],
                     cwd=ROOT, capture_output=True, text=True)
if res.returncode != 0:
    errors = [l for l in res.stdout.splitlines() if l.startswith("ERROR")]
    print(f"validate.py found problems in {rel} — fix them before continuing:\n" + "\n".join(errors[:20]), file=sys.stderr)
    sys.exit(2)
sys.exit(0)
