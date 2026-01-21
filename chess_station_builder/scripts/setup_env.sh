#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

uv venv --python 3.12
source .venv/bin/activate
uv pip install -e ".[dev]"

echo "Environment ready. Activate with: source .venv/bin/activate"
