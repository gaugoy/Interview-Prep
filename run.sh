#!/usr/bin/env bash
# Start the Interview Prep Viewer (see src/app/README.md).
set -euo pipefail
cd "$(dirname "$0")"
exec uvicorn src.app.main:app --reload --reload-dir src "$@"
