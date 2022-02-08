#!/bin/sh

set -e
trap '[ $? -eq 0 ] && exit 0 || echo "$0 FAILED"' EXIT

# bash gen-deps.sh
bash linting.sh
bash gen-doc.sh

echo "unit testing..."
poetry run pytest
poetry run coverage-badge -f -o doc/coverage.svg

exit 0
