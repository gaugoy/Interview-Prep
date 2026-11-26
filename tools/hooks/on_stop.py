#!/usr/bin/env python3
"""Claude Code Stop hook.

If content markdown changed in this working tree: rebuild the index (catalog.json,
INDEX.md, AGENT_INDEX counts) and validate the changed files. On validation errors it
exits 2 so the agent keeps working until they're fixed (skipped when the agent is already
continuing because of this hook, to avoid loops). Otherwise prints a short status line.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WATCHED = ("Python/", "Django DRF/", "Django ORM/", "Django ORM Short/", "django/", "React/")

try:
    payload = json.load(sys.stdin)
except Exception:
    payload = {}
if payload.get("stop_hook_active"):
    sys.exit(0)

status = subprocess.run(["git", "status", "--porcelain", "-uall"], cwd=ROOT, capture_output=True, text=True).stdout
changed = [l[3:].split(" -> ")[-1].strip().strip('"') for l in status.splitlines()]
content = [p for p in changed if p.endswith(".md") and p.startswith(WATCHED)]
if not content:
    sys.exit(0)

tools = ROOT / "tools"
subprocess.run([sys.executable, str(tools / "build_index.py")], cwd=ROOT, capture_output=True, text=True)
res = subprocess.run([sys.executable, str(tools / "validate.py"), "--changed"], cwd=ROOT, capture_output=True, text=True)
if res.returncode != 0:
    errors = [l for l in res.stdout.splitlines() if l.startswith("ERROR")]
    print("Content validation failed — fix before finishing:\n" + "\n".join(errors[:25]), file=sys.stderr)
    sys.exit(2)
print(json.dumps({"systemMessage": f"Index rebuilt; {len(content)} changed content file(s) validated."}))
sys.exit(0)
