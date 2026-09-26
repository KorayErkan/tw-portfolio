#!/bin/sh
# Regenerate the HTML version of every standalone Markdown sample with pandoc.
# Links to other .md files are rewritten to .html by the same filter the
# GitHub Pages build uses. Run from the repository root:  sh etc/scripts/build-md.sh
set -e
root=$(pwd)
filter="$root/.github/pages/links.lua"

for md in \
  src/api-documentation/parsing-web-requests-kozmos.md \
  src/api-documentation/parsing-web-requests-javascript.md \
  src/installation-guide/installation-guide.md \
  src/reference-charts/config-reference-chart.md \
  src/reference-charts/lang-reference-chart.md \
  src/release-notes/release-notes.md \
  src/system-configuration-guide/system-configuration-guide.md \
  src/tutorials/advanced-git-tutorial.md \
  src/tutorials/command-line-tutorial.md
do
  dir=$(dirname "$md"); name=$(basename "$md" .md)
  title=$(grep -m1 '^# ' "$md" | sed 's/^# //; s/[*_]//g')
  (cd "$dir" && pandoc "$name.md" -f markdown -t html5 -s \
     --lua-filter "$filter" --css ../css/common-light.css \
     --metadata pagetitle="$title" -o "$name.html")
  echo "built $dir/$name.html"
done
