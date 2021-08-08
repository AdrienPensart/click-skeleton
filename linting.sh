#!/bin/bash

set -e

echo "lint : pylint..."
poetry run pylint click_skeleton examples tests

echo "lint : flake8..."
poetry run flake8 click_skeleton examples tests

echo "static type checking : mypy..."
poetry run mypy click_skeleton examples tests
