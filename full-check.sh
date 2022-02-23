#!/bin/sh

set -e
trap '[ $? -eq 0 ] && exit 0 || echo "$0 FAILED"' EXIT

# bash gen-deps.sh
sh linting.sh
sh gen-doc.sh

echo "unit testing..."
poetry run pytest
poetry run coverage-badge -f -o doc/coverage.svg

sh code-format.sh
sh security-checks.sh

exit 0
