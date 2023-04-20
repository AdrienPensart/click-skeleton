#!/bin/sh

export SETUPTOOLS_USE_DISTUTILS=stdlib

set -e

poetry run isort click_skeleton examples tests
poetry run black click_skeleton examples tests
