#!/bin/sh

export SETUPTOOLS_USE_DISTUTILS=stdlib

set -e

sh code-format.sh

echo "lint : ruff..."
poetry run ruff check click_skeleton examples tests

echo "lint : pylint..."
poetry run pylint click_skeleton examples tests

echo "lint : flake8..."
poetry run flake8 click_skeleton examples tests

echo "static type checking : mypy..."
poetry run mypy click_skeleton examples tests

echo "static type checking : pyright..."
poetry run pyright
