#!/usr/bin/env python3
"""Random daily Facebook schedule. Usage: plan.py inbox|adds -> prints GO or SKIP."""
import json, os, random, sys
from datetime import datetime
from zoneinfo import ZoneInfo
now = datetime.now(ZoneInfo("America/Toronto"))
today = now.strftime("%Y-%m-%d")
path = f"/workspace/facebook-stats/plan-{today}.json"
def mins(h, m): return h * 60 + m
def fmt(t): return f"{t//60:02d}:{t%60:02d}"
def make():
    rnd = random.Random()
    n = rnd.randint(5, 7)
    while True:
        ts = sorted(rnd.randint(mins(8, 0), mins(21, 30)) for _ in range(n))
        if all(b - a >= 75 for a, b in zip(ts, ts[1:])): break
    adds = rnd.randint(mins(9, 0), mins(9, 45))
    return {"inbox": [{"t": fmt(t), "done": False} for t in ts],
            "adds": [{"t": fmt(adds), "done": False}]}
plan = json.load(open(path)) if os.path.exists(path) else make()
if not os.path.exists(path): json.dump(plan, open(path, "w"), indent=1)
kind = sys.argv[1]; cur = mins(now.hour, now.minute)
for s in plan[kind]:
    h, m = map(int, s["t"].split(":"))
    if not s["done"] and mins(h, m) <= cur:
        s["done"] = True; json.dump(plan, open(path, "w"), indent=1)
        print(f"GO (planned {s['t']}, now {fmt(cur)})"); sys.exit(0)
if kind == "adds" and all(s["done"] for s in plan["adds"]) and cur <= mins(15, 45):
    d = json.load(open("/workspace/facebook-stats/data.json"))
    g = d.get("goals", {})
    short = any(d["tracks"][k]["days"].get(today, {}).get("follows", 0) < (g.get(k, {}).get("daily", 8 if k == "regular" else 2) if isinstance(g.get(k), dict) else (8 if k == "regular" else 2)) for k in ("regular", "professionals"))
    last = plan.get("last_extra", plan["adds"][-1]["t"]); lh, lm = map(int, last.split(":"))
    if short and cur - mins(lh, lm) >= 55:
        plan["last_extra"] = fmt(cur); json.dump(plan, open(path, "w"), indent=1)
        print(f"GO (extra catch-up session: daily goal not met, now {fmt(cur)})"); sys.exit(0)
nxt = [s["t"] for s in plan[kind] if not s["done"]]
print("SKIP - next planned: " + (nxt[0] if nxt else "none left today"))
