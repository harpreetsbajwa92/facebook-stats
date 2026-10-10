# Facebook Stats
Live: https://harpreetsbajwa92.github.io/facebook-stats/ (repo harpreetsbajwa92/facebook-stats, GitHub Pages from main).
Dark, mobile-first. Page fetches data.json live (cache-busted, refreshes every 60s). All dates are Toronto dates.

## Tabs (layout rebuilt to match the LinkedIn Stats app)
- **Today** – header Regular / Professionals toggle, day ‹ › navigation, KPI grid (Follows done, Requests accepted + rate, Texts sent, Active chats), daily goal progress bar (8 regular / 2 professionals), People followed list with status, Good prospects.
- **Trends** – Regular / Professionals / Combined filter; Weekly / Monthly / Yearly with ‹ › period navigation; summary, accept & reply rate, days hit goal, streaks, goal projection; bar charts (follows, accepted, texts, active chats); all-time totals.
- **History** – day list newest first with same filter (Combined shows Reg+Pro split, green = goal hit); tap a day for handles.
- **Settings (⚙)** – how stats update, export JSON, goals.
- Footer line "App version: …" and no-cache meta tags; page re-fetches data.json every 60s.

## Good prospects
Never deleted automatically. **Only Harpreet may remove entries** (the Delete button on the page only hides it on his device; the data stays in data.json). Do not remove entries from data.json without his instruction.

## data.json
`tracks.<regular|professionals>` has `people`, `prospects`, and `days`: `{ "YYYY-MM-DD": {follows, accepted, texts, chats, flagged} }`.

## Update (all commands accept `--date YYYY-MM-DD` for backfill; default today, Toronto)
    python3 update.py add-follow regular somehandle "Some Name"
    python3 update.py add-follow professionals agenthandle "Name" --date 2026-10-08
    python3 update.py accepted somehandle      # followed back
    python3 update.py text somehandle          # text sent (call per text)
    python3 update.py chat somehandle          # active chat
    python3 update.py flag somehandle "short note" ["Name"]   # good prospect
    python3 update.py set-day regular --date 2026-10-07 --follows 8 --accepted 2 --texts 5 --chats 1 --flagged 0   # set/override a day
    python3 update.py show [--date D]
    ./publish.sh                               # git add/commit/push (uses gh credential helper)
Auth: gh CLI logged in as harpreetsbajwa92 (same as linkedin-stats). No phone numbers in data.json.

Auto-refresh: publish.sh stamps BUILD in index.html, footer, and version.json each publish; page polls version.json and reloads with ?v=<build>. Always publish via ./publish.sh.
