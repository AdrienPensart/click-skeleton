#!/bin/sh

export SETUPTOOLS_USE_DISTUTILS=stdlib

set -e

echo "doc generation (rst)..."
echo "rst-linting pass 1..."
poetry run rstcheck doc/help.rst
\cp doc/help.rst README.rst
poetry run examples/main.py readme >> README.rst
echo "rst-linting pass 2..."
poetry run rstcheck README.rst

echo "doc generation (markdown)..."
poetry run examples/main.py readme --output markdown > README.md

echo "doc linting (markdown)..."
poetry run mdformat --check ./*.md
