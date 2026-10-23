# Verifier Independence Calibration — Predeclared Protocol
# Freeze this file BEFORE the run. Do not edit after results. If a threshold
# is wrong, amend in a v2 file and re-run; do not move the goalpost mid-run.
# Adopted 2026-10-23 (reconciled from third-party audit paste; remediation for
# claims.yaml ids verifier_independence_operator / verifier_independence_empirical /
# rubber_stamp_resistance).

## Design
- N = 30 tasks per verifier pair.
- Split: 15 valid (should pass), 15 invalid.
  - Of the 15 invalid: 10 "plausible-bad" (subtle errors, not obviously broken)
    and 5 "obvious-bad" (control).
- Injection: through the normal selector, not an audit path.
- Blind: verifiers cannot see each other's verdicts; sealed bid.
- Rubric: versioned and pinned per verdict (`rubric_version` field required).

## Metrics (by verifier pair, published in full)
1. False-accept rate (FAR): passes on truly-invalid / 15.  Target: <= 0.05
2. False-reject rate (FRR): fails on truly-valid / 15.     Target: <= 0.10
3. Pairwise correlation: Cohen's kappa on their 30 verdicts. Target: <= 0.30
   - kappa > 0.30 => pair is NOT empirically independent regardless of
     credential diversity. Report it as such in the dossier.
4. Plausible-bad detection: passes that should have been fails on the 10
   plausible-bad subset. This is the rubber-stamp signal.
   Target: <= 1 pass out of 10 per pair.

## Predeclared thresholds (edit here ONLY before the run)
| metric            | threshold | action if exceeded |
|-------------------|-----------|--------------------|
| FAR               | 0.05      | pair not eligible for payout |
| FRR               | 0.10      | flag; investigate over-rejection |
| kappa             | 0.30      | pair reported as dependent |
| plausible-bad miss| 1 / 10    | pair not eligible for payout |

## Publication rules
- All pairs published, including failing ones.
- Report per-pair kappa, FAR, FRR, and plausible-bad count.
- No aggregation that hides a failing pair.
- Include a "known-bad that passed" table with task IDs.
- Negative result is a valid result. Publish it.

## Sample-size honesty
- 30 tasks/pair gives ~+/-0.08 on FAR. Treat 0.05 as directional, not
  exact. N=100 per pair if a regulator-grade number is needed.
- Cohen's kappa needs careful interpretation when verdict distributions are
  imbalanced; report the raw confusion matrix alongside kappa so readers can
  see what drives it.
