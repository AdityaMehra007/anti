# 🛡️ IMMUTABLE TRANSACTION LEDGER

## State Machine
```
CREATED ➔ VALIDATED ➔ APPROVAL_REQUIRED ➔ APPROVED ➔ QUEUED ➔ ATTEMPTED ➔ EXTERNAL_ACK ➔ EXTERNAL_REFERENCE ➔ RESPONSE_RECEIVED ➔ RECONCILED ➔ VERIFIED
```

## Schema & Cryptographic Hashing
Every transaction computes:
* `request_hash = SHA256(json.dumps(request_payload))`
* `response_hash = SHA256(json.dumps(response_payload))`
* Append-only transition events logged to `transaction_events` table in `data/omega_ledger.db`.
