#!/bin/sh
# Check every CSDB object: schema validation, then the layered BREX and SNS checks.
# Fails if any check reports an error. s1kd-validate and s1kd-brexcheck can exit 0 on
# failure (and s1kd-validate prints SUCCESS when it can't load a schema), so the output
# is scanned for ERROR lines instead of trusting their exit codes.
#
# Needs s1kd-tools, the Issue 7 flat schemas in etc/s1000d-schemas/ at the repository root, and the
# Issue 7 default BREX from the s1kd-tools source (S1KD_BREX_DIR).
#
# Usage: sh tools/check.sh   (from the sample root)

set -u
cd "$(dirname "$0")/../csdb" || exit 2
BREX_DIR="${S1KD_BREX_DIR:-$HOME/s1kd-tools/tools/s1kd-brexcheck/brex}"
LOG=$(mktemp)

s1kd-validate --xml-catalog ../tools/catalog.xml DMC-*.XML PMC-*.XML >"$LOG" 2>&1
s1kd-brexcheck -I "$BREX_DIR" -l -c -S -s DMC-*.XML PMC-*.XML >>"$LOG" 2>&1

if grep -q "ERROR" "$LOG"; then
    grep "ERROR" "$LOG"
    rm -f "$LOG"
    echo "FAILED"
    exit 1
fi
rm -f "$LOG"
echo "OK: $(ls DMC-*.XML | wc -l) data modules and $(ls PMC-*.XML | wc -l) publication module pass schema, BREX and SNS checks"
