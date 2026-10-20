# Shim Math oracle: independent integer mirror of engine.js (min-count DP done differently). Writes expected.json.
import json
from math import gcd
from functools import reduce
from itertools import combinations_with_replacement

GAP = "the gap must be from 0.01 to 50 mm with at most two decimal places"
KIT = "each shim thickness must be from 0.01 to 10 mm with at most two decimal places, up to 8 sizes"
LIST = "each shim in the stack must be from 0.01 to 10 mm with at most two decimal places, up to 12 shims"

def p(t, err, lo, hi):
    t = t.strip()
    parts = t.split(".")
    if len(parts) > 2 or not parts[0].isdigit() or (len(parts) == 2 and (not parts[1].isdigit() or len(parts[1]) > 2)):
        raise ValueError(err)
    v = int(parts[0]) * 100 + int(parts[1].ljust(2, "0")) if len(parts) == 2 else int(parts[0]) * 100
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def plist(t, err, maxn, dedupe=True):
    parts = [s.strip() for s in t.strip().split(",") if s.strip() != ""]
    if len(parts) < 1 or len(parts) > maxn:
        raise ValueError(err)
    out = []
    for s in parts:
        v = p(s, err, 1, 1000)
        if dedupe and v in out:
            continue
        out.append(v)
    return out

def dec(v):
    s, f = str(v // 100), str(v % 100).rjust(2, "0").rstrip("0")
    return s + "." + f if f else s

def mm(v): return dec(v) + " mm"

def stacktext(xs): return " + ".join(mm(x) for x in xs)
def kittext(xs): return ", ".join(mm(x) for x in xs)

def stackTruth(gap, lst):
    g = p(gap, GAP, 1, 5000); xs = plist(lst, LIST, 12, dedupe=False)
    tot = sum(xs)
    s = "Your stack of " + stacktext(xs) + " adds up to " + mm(tot) + ". The gap is " + mm(g) + ", so "
    if tot == g: return s + "the stack fills it exactly."
    if tot < g: return s + mm(g - tot) + " stays unfilled."
    return s + "the stack stands " + mm(tot - g) + " proud of the gap."

def _best(xs, g):
    # independent search: try all counts up to a bound via DP on reachable min count (BFS layers)
    INF = float("inf")
    dp = [INF] * (g + 1); dp[0] = 0; frm = [-1] * (g + 1)
    for w in range(g + 1):
        if dp[w] >= INF: continue
        for x in xs:
            nv = w + x
            if nv <= g and dp[w] + 1 < dp[nv]:
                dp[nv] = dp[w] + 1; frm[nv] = x
    best = g
    while best > 0 and dp[best] >= INF: best -= 1
    used = []
    cur = best
    while cur > 0:
        used.append(frm[cur]); cur -= frm[cur]
    return best, sorted(used, reverse=True)

def pickTruth(gap, kit):
    g = p(gap, GAP, 1, 5000); xs = plist(kit, KIT, 8)
    best, used = _best(xs, g)
    if best == 0:
        return "No stack from the kit of " + kittext(sorted(xs)) + " fits inside a " + mm(g) + " gap at all."
    u = stacktext(used[:12]) + " + …" if len(used) > 12 else stacktext(used)
    s = "From the kit " + kittext(sorted(xs)) + ", the fewest shims for a " + mm(g) + " gap: " + u + " (" + str(len(used)) + (" shim" if len(used) == 1 else " shims") + "). "
    if best == g: return s + "That fills the gap exactly."
    return s + "That leaves " + mm(g - best) + " the kit cannot reach."

def stepTruth(gap, kit):
    g = p(gap, GAP, 1, 5000); xs = plist(kit, KIT, 8)
    d = reduce(gcd, xs)
    s = "The kit " + kittext(sorted(xs)) + " steps in multiples of " + mm(d) + ". "
    if g % d == 0:
        return s + "The " + mm(g) + " gap is a whole multiple, so an exact stack exists if the kit is deep enough."
    below = g - (g % d)
    return s + "The " + mm(g) + " gap is not a whole multiple; the nearest exact hits are " + mm(below) + " below and " + mm(below + d) + " above."

FNS = {"stackTruth": stackTruth, "pickTruth": pickTruth, "stepTruth": stepTruth}

cases = []
gaps = ["0.01", "0.3", "1.85", "1.87", "12.34", "50"]
kits = ["0.05, 0.1, 0.2, 0.5, 1", "0.01", "0.25, 0.75", "2, 3", "0.1, 0.3"]
for g in gaps:
    for k in kits:
        cases.append(("pickTruth", [g, k])); cases.append(("stepTruth", [g, k]))
stacks = [("1.85", "1, 0.5, 0.2, 0.1, 0.05"), ("0.01", "0.02"),
          ("5", "2, 2, 2"), ("0.5", "0.5, 0.5"), ("12.34", "10, 2, 0.3, 0.04"), ("1", "0.1")]
for g, l in stacks:
    cases.append(("stackTruth", [g, l]))
errs = [("0", "1"), ("50.01", "1"), ("1.234", "1"),
        ("1", "0"), ("1", "10.01"), ("1", "1.234"), ("1", ", ,"), ("1", "1, 1, 1, 1, 1, 1, 1, 1, 1")]
out = []
for name, args in cases:
    fn = FNS[name]
    try: exp = fn(*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": name, "args": args, "expected": exp})
for args in errs:
    for name in ("pickTruth", "stackTruth"):
        fn = FNS[name]
        try: exp = fn(*args)
        except ValueError as e: exp = "ERR:" + str(e)
        out.append({"fn": name, "args": args, "expected": exp})
with open("expected.json", "w") as fh:
    json.dump(out, fh, indent=1)
print(len(out), "cases written")
