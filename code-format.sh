#!/bin/sh

export SETUPTOOLS_USE_DISTUTILS=stdlib

set -e

poetry run isort code_skeleton examples tests
