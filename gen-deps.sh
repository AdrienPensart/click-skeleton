#!/bin/bash

set -e

echo "updating poetry deps..."
poetry update

echo "generating setup.py..."
# poetry run dephell convert
poetry run poetry2setup > setup.py

echo "requirements.txt generation..."
# poetry run dephell deps convert --from-format=poetry --from-path=pyproject.toml --to-format=pip --to-path=requirements.txt --envs main
poetry export -f requirements.txt --without-hashes -o requirements.txt

echo "requirements-dev.txt generation..."
# poetry run dephell deps convert --from-format=poetry --from-path=pyproject.toml --to-format=pip --to-path=requirements-dev.txt --envs main dev
poetry export -f requirements.txt --dev --without-hashes -o requirements-dev.txt
