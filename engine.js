// Shim Math engine: shim stack totals against a gap, the fewest shims from a kit that hit it, and the kit's finest step. Exact integers (hundredths of a mm), half-up only on display.
function _p(t, err, intDigits, places, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _GAP = "the gap must be from 0.01 to 50 mm with at most two decimal places";
var _KIT = "each shim thickness must be from 0.01 to 10 mm with at most two decimal places, up to 8 sizes";
var _LIST = "each shim in the stack must be from 0.01 to 10 mm with at most two decimal places, up to 12 shims";
function _plist(t, err, max, dedupe) {
  t = typeof t === "string" ? t.trim() : "";
  var parts = t.split(",").map(function (s) { return s.trim(); }).filter(function (s) { return s !== ""; });
  if (parts.length < 1 || parts.length > max) throw new Error(err);
  var seen = {}, out = [];
  for (var i = 0; i < parts.length; i++) {
    var v = _p(parts[i], err, 2, 2, 1, 1000);
    if (dedupe && seen[v]) continue;
    seen[v] = 1; out.push(v);
  }
  return out;
}
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _mm(v) { return _dec(v, 2) + " mm"; }
function _gcd(a, b) { while (b) { var t = a % b; a = b; b = t; } return a; }
function _stacktext(list) {
  if (list.length === 1) return _mm(list[0]);
  return list.map(_mm).join(" + ");
}
function _kittext(list) {
  return list.map(_mm).join(", ");
}

function stackTruth(gap, list) {
  var g = _p(gap, _GAP, 2, 2, 1, 5000), xs = _plist(list, _LIST, 12, false);
  var tot = xs.reduce(function (a, b) { return a + b; }, 0);
  var s = "Your stack of " + _stacktext(xs) + " adds up to " + _mm(tot) + ". The gap is " + _mm(g) + ", so ";
  if (tot === g) return s + "the stack fills it exactly.";
  if (tot < g) return s + _mm(g - tot) + " stays unfilled.";
  return s + "the stack stands " + _mm(tot - g) + " proud of the gap.";
}
function pickTruth(gap, kit) {
  var g = _p(gap, _GAP, 2, 2, 1, 5000), xs = _plist(kit, _KIT, 8, true);
  // exact min-count unbounded knapsack via DP over 0..g
  var INF = 1e9, dp = [0], from = [-1];
  for (var v = 1; v <= g; v++) { dp[v] = INF; from[v] = -1; }
  for (var w = 0; w < g; w++) {
    if (dp[w] >= INF) continue;
    for (var i = 0; i < xs.length; i++) {
      var nv = w + xs[i];
      if (nv <= g && dp[w] + 1 < dp[nv]) { dp[nv] = dp[w] + 1; from[nv] = xs[i]; }
    }
  }
  var best = g;
  while (best > 0 && dp[best] >= INF) best--;
  if (best === 0) return "No stack from the kit of " + _kittext(xs.slice().sort(function(a,b){return a-b;})) + " fits inside a " + _mm(g) + " gap at all.";
  var used = [], cur = best;
  while (cur > 0) { used.push(from[cur]); cur -= from[cur]; }
  used.sort(function (a, b) { return b - a; });
  var u = used.length > 12 ? _stacktext(used.slice(0, 12)) + " + …" : _stacktext(used);
  var s = "From the kit " + _kittext(xs.slice().sort(function(a,b){return a-b;})) + ", the fewest shims for a " + _mm(g) + " gap: " + u + " (" + used.length + (used.length === 1 ? " shim" : " shims") + "). ";
  if (best === g) return s + "That fills the gap exactly.";
  return s + "That leaves " + _mm(g - best) + " the kit cannot reach.";
}
function stepTruth(gap, kit) {
  var g = _p(gap, _GAP, 2, 2, 1, 5000), xs = _plist(kit, _KIT, 8, true);
  var d = xs.reduce(function (a, b) { return _gcd(a, b); });
  var s = "The kit " + _kittext(xs.slice().sort(function(a,b){return a-b;})) + " steps in multiples of " + _mm(d) + ". ";
  if (g % d === 0) return s + "The " + _mm(g) + " gap is a whole multiple, so an exact stack exists if the kit is deep enough.";
  var below = g - (g % d), above = below + d;
  return s + "The " + _mm(g) + " gap is not a whole multiple; the nearest exact hits are " + _mm(below) + " below and " + _mm(above) + " above.";
}
