#!/bin/sh

set -e

echo "security checks : bandit..."
poetry run bandit -r click_skeleton -s B604,B101,B608,B108

echo "security checks : safety..."
poetry run safety check
