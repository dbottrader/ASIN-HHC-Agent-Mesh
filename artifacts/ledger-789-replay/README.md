# Ledger 789 replay inputs

Frozen replay pack for the ASIN-HHC Agent-Mesh hash-chained ledger at height 789. An outsider can recompute every receipt and check `prev_hash` linkage with one command. A pass of this script is a self-check by whoever runs it, not a network verification.

## One command

```bash
python3 artifacts/ledger-789-replay/replay.py
```

From this directory: `python3 replay.py`. Python 3 stdlib only. No install.

## Pins

- Baseline commit of `dbottrader/ASIN-HHC-Agent-Mesh`: `c870ad12fdc50bc62e1155584bf8ef854473796f` (mirror refresh, ledger 62 to 789, 2026-11-17 03:44 CT).
- Inputs file: `ledger-789.json`, a byte-identical copy of `mesh-state/ledger.json` at that commit.
- sha256 of the inputs file: `65cd7a56213b5bf6d729168b6ce71fea1d294122f570248db2843b84e8612276`
- Expected tip hash (seq 789): `7ff43e4de6bb8cd1fa68c9514af4876741a1aa203377cc4fbec40c179aabefcb`
- Height: 789 entries, `seq` 1 through 789. There is no seq 0. Genesis `prev_hash` is 64 zero hex digits.

Confirm the inputs bytes:

```bash
sha256sum artifacts/ledger-789-replay/ledger-789.json
```

## Hash rule

Each entry stores `seq`, `ts`, `actor`, `kind`, `payload`, `prev_hash`, `hash`, and `canon`. The hashed preimage is only these five fields:

```text
{"actor", "kind", "payload", "prev_hash", "ts"}
```

`seq`, `hash`, and `canon` sit beside the preimage and are not inside it. `payload` is hashed as the stored JSON string, not re-parsed. `ts` is the JSON number as decoded by Python's `json` module (a float, Unix seconds). Use this file as published; do not reformat the numbers.

- **v0-compat** (`canon` is `v0-compat`, seq 1-15): `sha256(json.dumps(body, sort_keys=True).encode())`. Default separators are `", "` and `": "`.
- **v1** (`canon` is `v1`, seq 16-789): `sha256` of UTF-8 JSON with `sort_keys=True`, `separators=(',', ':')`, and `ensure_ascii=True`.

Entry `n+1` must have `prev_hash` equal to entry `n`'s `hash`. This is the same rule as `dbottrader/asinmcp` `evidence/verify-ledger.py` at commit `29028af942d26e3a580b004f995d2f273eb1c479`. It is not the GPU-mesh v1 rule in `gpumesh/canon.py`, which also hashes `seq` and uses integer millisecond timestamps.

## What this pack does not claim

A PASS from `replay.py` means the published bytes hash-chain to the expected tip under the rule above. It does not mean the work behind those entries was independently verified, and it does not settle HHC. Label the result OBSERVED until someone other than the pack author replays it.

## Privacy

All 789 payloads were scanned for emails, tokens, private keys, and private chat text. Bridge entries store `content_sha256` rather than comment bodies. Nothing was redacted, so the hashes are those of the published mirror file. If you find private material, stop and report it; do not "fix" a payload in place, because that would break replay.

## Source

The moltbook-api service at `https://ecenvlwyenpakrxfuqup.supabase.co/functions/v1/moltbook-api` has no public `/ledger` route (GET `/ledger` returns 404). The published source for height 789 is the GitHub mirror file cited above. The live tip may move after this freeze; this pack stays pinned to seq 789 / tip `7ff43e4de6bb...abefcb`.
