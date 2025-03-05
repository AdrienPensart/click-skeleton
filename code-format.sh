#!/bin/sh

set -e

uv run isort click_skeleton examples tests
uv run black click_skeleton examples tests
