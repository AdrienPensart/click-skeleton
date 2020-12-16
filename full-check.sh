#!/bin/sh
set -e
trap '[ $? -eq 0 ] && exit 0 || echo "$0 FAILED"' EXIT

echo "updating poetry deps..."
poetry update

echo "generating setup.py..."
poetry run dephell convert

echo "requirements.txt generation..."
poetry run dephell deps convert --from-format=poetry --from-path=pyproject.toml --to-format=pip --to-path=requirements.txt --envs main

echo "requirements-dev.txt generation..."
poetry run dephell deps convert --from-format=poetry --from-path=pyproject.toml --to-format=pip --to-path=requirements-dev.txt --envs main dev

echo "lint : pylint..."
poetry run pylint click_skeleton examples tests

echo "lint : flake8..."
poetry run flake8 click_skeleton examples tests

echo "static type checking : mypy..."
poetry run mypy --strict click_skeleton examples tests

# re-enable this when pytype supports python 3.9 : https://github.com/google/pytype/issues/749
# echo "static type checking : pytype..."
# poetry run pytype click_skeleton examples tests -j auto -k

poetry run pytest
poetry run coverage-badge -f -o doc/coverage.svg

exit 0
