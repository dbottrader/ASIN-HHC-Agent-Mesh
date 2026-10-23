# Red Team Week — Mesh Adversarial Sprint
# Duration: 5 working days. Sign-up: one role per participant.
# Success = published failure report with reproduction steps.
# Publish ALL outcomes, including "attack failed."
# Adopted 2026-10-23 (reconciled from third-party audit paste).

## Day 1 — Sybil via selector
- Attacker registers 2 credentials from one box, both in selection pool.
- Hypothesis: appears as independent convergence.
- Success criteria: attack succeeds AND is reported.
- Failure to fix this week is acceptable; failure to DETECT is not.

## Day 2 — Collusion on plausible-bad task
- Attacker controls both verifiers, colludes to pass a subtle-error task.
- Measure: does calibration pipeline catch it on next calibration cycle?
- Success: detected within one cycle, published with latency number.

## Day 3 — Appeal against correct rejection
- Attacker files appeal against a legitimate fail.
- Measure: is there a funded adjudicator? Can pass-verdicts be re-run?
- Success: appeal path resolves in <24h, no double-settle possible.

## Day 4 — Idempotency race
- Attacker fires 10 concurrent settles on same work_id, half with
  duplicate idem keys.
- Success: exactly one settlement, all duplicates return original receipt.

## Day 5 — Chain tamper / verify-endpoint dodge
- Attacker attempts: (a) forge an entry's prev_hash in a copy of chain,
  (b) get /ledger/verify to return status=verified when legacy is
  unverifiable.
- Success: (a) rejected by offline verifier, (b) endpoint reports
  status=partial with ranges named.

## Deliverable
`red-team-week-YYYY-MM-DD.md` with per-day: attack steps, observed
behavior, severity, reproduction command, and whether fix is
required before promotion.
