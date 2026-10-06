# EcoGrid Energy — Python demonstration repository

A small, runnable **educational prototype** for a peer-to-peer energy trading workflow. It demonstrates trade creation, meter verification, and idempotent settlement using Python's standard library and SQLite. **It is not a production payment system or a deployed integration.**

## Requirements
Python 3.10+; no third-party dependencies for the core demo.

## Run
```bash
python demo.py
python -m unittest discover -s tests -v
```

## Repository layout
- `marketplace/` — create and inspect trades
- `smart_meter/` — record and verify energy delivery
- `settlement/` — settle verified trades with idempotency
- `shared/` — SQLite persistence and shared workflow
- `tests/` — unit tests
- `docs/` — architecture and team workflow
- `.github/workflows/` — GitHub Actions checks

## Limitations
This local prototype uses a single SQLite database and synchronous calls. A production architecture would use service-owned databases, an outbox, an event broker, durable retries, reconciliation, access controls, and a real payment provider. No genuine GitHub or Monday.com activity is implied by this starter repository.

## Security
Do not commit credentials, real payment details, customer data, or local `.db` files. Use test-only data.
