#!/usr/bin/env bash
# Publish Facebook Stats to GitHub Pages (https://harpreetsbajwa92.github.io/facebook-stats/)
set -e
cd "$(dirname "$0")"
# Stamp build version (version.json + BUILD + footer in index.html) on every publish
python3 - <<'PY'
import re, json, datetime
n = datetime.datetime.now()
v = n.strftime("%Y%m%d%H%M%S")
label = n.strftime("%b %-d, %-I:%M %p")
s = open("index.html").read()
s = re.sub(r'const BUILD="[^"]*";', 'const BUILD="%s";' % v, s)
s = re.sub(r'(<span id="appVer">)[^<]*(</span>)', r'\g<1>%s (build %s)\g<2>' % (label, v), s)
open("index.html", "w").write(s)
json.dump({"v": v}, open("version.json", "w")); open("version.json", "a").write("\n")
PY
git add -A
if git diff --cached --quiet; then echo "no changes"; exit 0; fi
git commit -qm "Update stats $(date '+%Y-%m-%d %H:%M')"
git push -q origin main
echo "published"
