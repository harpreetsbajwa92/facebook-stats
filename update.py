#!/usr/bin/env python3
"""Update data.json. Every action records into a per-day row (Toronto date).
Add  --date YYYY-MM-DD  anywhere to backfill (default: today, Toronto).

  update.py add-follow <regular|professionals> <handle> [name]
  update.py accepted <handle>              (they followed back / accepted)
  update.py text <handle>                  (a text was sent; call per text)
  update.py chat <handle>                  (mark active chat)
  update.py flag <handle> "note" [name]    (good prospect)
  update.py set-day <regular|professionals> [--date D] [--follows N] [--accepted N]
                    [--texts N] [--chats N] [--flagged N]   (set/override a day's numbers)
  update.py show [--date D]
"""
import json, sys, os, datetime
from zoneinfo import ZoneInfo
TZ = ZoneInfo("America/Toronto")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
d = json.load(open(P))
KEYS = ["follows", "accepted", "texts", "chats", "flagged"]
a = sys.argv[1:]
def opt(name, default=None):
    if name in a:
        i = a.index(name); v = a[i+1]; del a[i:i+2]; return v
    return default
day = opt("--date") or datetime.datetime.now(TZ).date().isoformat()
datetime.date.fromisoformat(day)
h = lambda s: s.strip().lstrip("@").lower()

# migrate older structure (no per-day rows)
for t, tr in d["tracks"].items():
    tr.setdefault("days", {})
    for p in tr["people"]:
        if p.get("chat") and not p.get("chatDate"): p["chatDate"] = p.get("accepted") or p["followed"]
    if not tr["days"]:
        for p in tr["people"]:
            row = lambda k: tr["days"].setdefault(k, dict.fromkeys(KEYS, 0))
            row(p["followed"])["follows"] += 1
            if p["accepted"]: row(p["accepted"])["accepted"] += 1
            for x in p["texts"]: row(x)["texts"] += 1
            if p.get("chatDate"): row(p["chatDate"])["chats"] += 1
        for x in tr["prospects"]:
            tr["days"].setdefault(x["date"], dict.fromkeys(KEYS, 0))["flagged"] += 1
def bump(t, k, n=1):
    r = d["tracks"][t]["days"].setdefault(day, dict.fromkeys(KEYS, 0)); r[k] += n

def find(handle):
    for t, tr in d["tracks"].items():
        for p in tr["people"]:
            if p["handle"] == handle: return t, p
    sys.exit(f"unknown handle {handle}; add-follow first")

if not a: sys.exit(__doc__)
c = a[0]
if c == "add-follow":
    t, hd = a[1], h(a[2])
    if t not in d["tracks"]: sys.exit("track must be regular or professionals")
    for tr in d["tracks"].values():
        if any(p["handle"] == hd for p in tr["people"]): sys.exit("already tracked")
    d["tracks"][t]["people"].append({"handle": hd, "name": a[3] if len(a) > 3 else "", "followed": day, "accepted": None, "texts": [], "chat": False, "chatDate": None})
    bump(t, "follows")
elif c in ("accepted", "text", "chat"):
    t, p = find(h(a[1]))
    if c == "accepted":
        if not p["accepted"]: p["accepted"] = day; bump(t, "accepted")
    elif c == "text": p["texts"].append(day); bump(t, "texts")
    elif not p["chat"]: p["chat"] = True; p["chatDate"] = day; bump(t, "chats")
elif c == "flag":
    t, p = find(h(a[1]))
    pr = d["tracks"][t]["prospects"]
    name = a[3] if len(a) > 3 else p.get("name", "")
    if not any(x["handle"] == p["handle"] for x in pr): bump(t, "flagged")
    pr[:] = [x for x in pr if x["handle"] != p["handle"]]
    pr.append({"handle": p["handle"], "name": name, "date": day, "note": a[2]})
elif c == "set-day":
    t = a[1]
    if t not in d["tracks"]: sys.exit("track must be regular or professionals")
    row = d["tracks"][t]["days"].setdefault(day, dict.fromkeys(KEYS, 0))
    for k in KEYS:
        v = opt("--" + k)
        if v is not None: row[k] = int(v)
elif c == "show":
    for t, tr in d["tracks"].items():
        r = tr["days"].get(day, dict.fromkeys(KEYS, 0))
        print(t, day, r, "| totals: people", len(tr["people"]), "prospects", len(tr["prospects"]))
    sys.exit()
else: sys.exit(__doc__)
d["updated"] = datetime.datetime.now(TZ).isoformat(timespec="seconds")
json.dump(d, open(P, "w"), indent=2)
print("ok", day)
