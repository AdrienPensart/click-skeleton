#!/bin/sh

set -e

sh code-format.sh

echo "lint : ruff..."
uv run ruff check click_skeleton examples tests

echo "lint : pylint..."
uv run pylint click_skeleton examples tests

echo "lint : flake8..."
uv run flake8 click_skeleton examples tests

echo "static type checking : mypy..."
uv run mypy click_skeleton examples tests

echo "static type checking : pyright..."
uv run pyright
