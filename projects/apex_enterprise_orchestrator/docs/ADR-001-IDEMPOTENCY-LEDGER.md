# ADR-001: Cryptographic Payload-Hashed Idempotency Ledger

## Status
Accepted

## Context
In distributed financial settlement and high-volume procurement ingestion, network timeouts and retries frequently cause duplicate POST requests. Executing reconciliation or approval twice results in catastrophic duplicate vendor payouts and ledger divergence.

## Decision
We implemented a SHA-256 payload-hashed idempotency ledger with atomic reservation semantics:
1. When an incoming request arrives with `X-Idempotency-Key`, compute `SHA256(canonical_json(payload))`.
2. Inspect the ledger under an async lock:
   - If key exists with **identical** hash and status `COMPLETED`: Return cached response immediately without re-executing.
   - If key exists with a **different** hash: Raise `409 Conflict` (key tampering / collision attack).
   - If key is currently in `PENDING` state: Raise `429 Too Many Requests` (concurrent in-flight duplicate).
   - If key does not exist or expired: Atomically reserve key in `PENDING` state.
3. Once upstream matching completes, update the key to `COMPLETED` with the serialized payload.
4. On unexpected error, clean up key to permit transparent retry.

## Consequences
- **Positive**: 100% protection against duplicate payments; deterministic response replication.
- **Trade-off**: Requires persistent storage and minimal hash computation overhead (<0.005ms).
