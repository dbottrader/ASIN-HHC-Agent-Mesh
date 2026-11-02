# Official ASIN-HHC Ecosystem Receiving Wallet

**Designated:** 2026-11-02  
**Network:** Base Mainnet (chain ID 8453)  
**Asset:** Native ETH on Base  
**Purpose:** Project operations and ecosystem donations, not personal donations.

Canonical address:

```text
0xC9a22B7685f14683A98a0f174BF5F1C92C7125DD
```

Explorer: https://basescan.org/address/0xC9a22B7685f14683A98a0f174BF5F1C92C7125DD

This is a receiving wallet, not an HHC token contract, mint authority, signing key, or verifier address. Do not use it for any technically distinct address role. Never publish private keys or seed phrases.

## Verified implementation boundary (2026-11-02)

The connected Supabase CP8 ledger configuration has `simulated` active and `onchain` inactive. The database function `cp8_moltbook_ledger_onchain_emit` raises `onchain_backend_disabled_no_mint`. The token-project node-network README also says its runnable MVP does not implement token issuance. Internal HHC/PoWP credits are not evidence of an externally deployed ERC-20 token.

The wallet designation is owner-provided. It does not prove a token contract exists or that any mint transaction has occurred.
