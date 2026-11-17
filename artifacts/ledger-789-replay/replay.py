#!/usr/bin/env python3
"""Replay the ASIN-HHC Agent-Mesh ledger hash chain (height 789).

Stdlib only. A passing run is a self-check, not an independent verification.

Usage:
    python3 replay.py
    python3 replay.py /path/to/ledger-789.json
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

GENESIS_PREV = "0" * 64
EXPECTED_TIP = "7ff43e4de6bb8cd1fa68c9514af4876741a1aa203377cc4fbec40c179aabefcb"
EXPECTED_HEIGHT = 789
HASHED_FIELDS = ("actor", "kind", "payload", "prev_hash", "ts")

# Hash rule, matching dbottrader/asinmcp@29028af942d26e3a580b004f995d2f273eb1c479
# evidence/verify-ledger.py:
#   v0-compat (seq 1-15): sha256(json.dumps(body, sort_keys=True))
#       default separators (', ', ': '), default ensure_ascii
#   v1 (seq 16+): sha256 of UTF-8 JSON with sort_keys=True,
#       separators=(',', ':'), ensure_ascii=True
# Preimage fields are actor, kind, payload, prev_hash, ts.
# seq, hash, and canon are not inside the preimage. payload is hashed
# as the stored string, not re-parsed.


def sha_v0_compat(body: dict) -> str:
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()


def sha_v1(body: dict) -> str:
    raw = json.dumps(
        body, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_entries(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("entries"), list):
        return data["entries"]
    if isinstance(data, list):
        return data
    raise SystemExit(f"unrecognized ledger format in {path}")


def replay(entries: list[dict]) -> tuple[bool, list[str], str | None]:
    errors: list[str] = []
    prev = GENESIS_PREV
    tip = None
    for index, entry in enumerate(entries, start=1):
        seq = entry.get("seq")
        if seq != index:
            errors.append(f"seq gap at {seq}, expected {index}")
        if entry.get("prev_hash") != prev:
            errors.append(f"link break at seq {seq}")
        try:
            body = {field: entry[field] for field in HASHED_FIELDS}
        except KeyError as exc:
            errors.append(f"missing {exc} at seq {seq}")
            prev = str(entry.get("hash") or "")
            tip = prev
            continue
        if entry.get("canon") == "v1":
            digest = sha_v1(body)
        else:
            digest = sha_v0_compat(body)
        if digest != entry.get("hash"):
            errors.append(f"hash mismatch at seq {seq}")
        prev = str(entry.get("hash") or "")
        tip = prev
    return (not errors and bool(entries), errors, tip)


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else script_dir / "ledger-789.json"
    if not path.is_file():
        print(f"FAIL: inputs file not found: {path}", file=sys.stderr)
        return 1
    entries = load_entries(path)
    ok, errors, tip = replay(entries)
    print(f"inputs={path}")
    print(f"rows={len(entries)}")
    print(f"tip={tip}")
    print(f"expected_tip={EXPECTED_TIP}")
    print(f"expected_height={EXPECTED_HEIGHT}")
    if len(entries) != EXPECTED_HEIGHT:
        errors.append(f"height {len(entries)} != expected {EXPECTED_HEIGHT}")
        ok = False
    if tip != EXPECTED_TIP:
        errors.append(f"tip {tip} != expected {EXPECTED_TIP}")
        ok = False
    if ok:
        print("result=PASS")
        print("label=SELF-CHECK")
        print("note=This pass is a self-check, not an independent verification.")
        return 0
    print("result=FAIL")
    print("label=SELF-CHECK")
    for err in errors:
        print(f"error={err}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
