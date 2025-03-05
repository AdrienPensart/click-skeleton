#!/bin/sh

set -e

echo "doc generation (rst)..."
echo "rst-linting pass 1..."
uv run rstcheck doc/help.rst
\cp doc/help.rst README.rst
uv run python -m examples.main readme >> README.rst
echo "rst-linting pass 2..."
uv run rstcheck README.rst

echo "doc generation (markdown)..."
uv run python -m examples.main readme --output markdown > README.md

echo "doc linting (markdown)..."
uv run mdformat --check ./*.md
