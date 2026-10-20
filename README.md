# Shim Math

Shim stack arithmetic. Your gap is 1.85 mm. The kit holds 0.05, 0.1, 0.2, 0.5 and 1 mm. Five shims fill it exactly: 1 + 0.5 + 0.2 + 0.1 + 0.05.

## What it computes

- **The stack truth** - what a picked stack of shims (0.01 to 10 mm each, up to 12) adds up to against a gap (0.01 to 50 mm): exact fill, unfilled, or standing proud.
- **The pick truth** - the fewest shims from a kit (up to 8 sizes) that fill the gap exactly, or the closest the kit reaches and what stays short.
- **The step truth** - the finest step the kit can hit exactly (the shared step of its sizes), and whether the gap is a whole multiple of it, with the nearest exact hits.

## Boundary

Arithmetic only. The gap and every thickness are the owner's own entries, every shim treated as flat and exact. It has not seen any job and does not know parts' flatness or wear, how shims compress under load, heat, or what gap is right for a machine, and it gives no verdict that a fit, an assembly or a machine is adequate or safe. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on hundredths of a mm, min-count DP for the pick).
- `oracle.py` - the Python mirror (independent integer DP) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/shimmath/
Repo: https://github.com/iLanis-agent/shimmath
