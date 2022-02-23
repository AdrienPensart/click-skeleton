#!/bin/sh

set -e

poetry run isort click_skeleton examples standard_examples tests
