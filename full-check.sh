#!/bin/sh

export SETUPTOOLS_USE_DISTUTILS=stdlib

set -e
trap '[ $? -eq 0 ] && exit 0 || echo "$0 FAILED"' EXIT

sh linting.sh
sh gen-doc.sh
sh code-format.sh

echo "unit testing..."
poetry run pytest
poetry run coverage-badge -f -o doc/coverage.svg

exit 0
