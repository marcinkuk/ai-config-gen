#!/usr/bin/env bash
# pypi-publish.sh — Quick publish to PyPI
# Usage: ./pypi-publish.sh
# Requires: PYPi_TOKEN env variable set
#
# To get a PyPI token:
# 1. Go to https://pypi.org/manage/account/token/
# 2. Create a new API token
# 3. Run: export PYPi_TOKEN="pypi-AgXXX..."
# 4. Run this script

set -euo pipefail
cd "$(dirname "$0")"

echo "📦 Publishing ai-config-gen to PyPI..."

# Build if dist doesn't exist
if [ ! -f "dist/ai_config_gen-*.tar.gz" ]; then
  echo "  Building distribution..."
  python -m build
fi

# Upload
if [ -z "${PYPI_TOKEN:-}" ]; then
  echo "❌ PYPI_TOKEN not set. Export it first: export PYPI_TOKEN='pypi-AgXXX...'"
  exit 1
fi

twine upload --skip-existing "dist/ai_config_gen-*" \
  --username __token__ \
  --password "${PYPI_TOKEN}"

echo "✅ Published to https://pypi.org/project/ai-config-gen/"