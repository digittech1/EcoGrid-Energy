# Architecture notes

## Demonstrated local workflow
1. Marketplace creates a trade in `PENDING_METER`.
2. Smart Meter Integration accepts unique reading events.
3. Verification advances the trade to `VERIFIED` only when readings cover agreed delivery.
4. Settlement records a mock payment and moves the trade to `SETTLED`.
5. Repeating a settlement with the same idempotency key returns the original record.

## Proposed production architecture (not implemented)
- Independent Marketplace, Smart Meter Integration and Financial Settlement services
- Kafka or comparable durable message broker
- Transactional outbox and Saga state machine
- Retry with exponential backoff, circuit breakers, dead-letter handling
- Payment gateway integration with status reconciliation
- Prometheus/Grafana metrics, OpenTelemetry traces and structured logs
- Service-owned databases, backup and disaster recovery

## Proposed indicators (not measured)
- Marketplace API P95 < 300 ms
- Event processing P95 < 5 s
- Zero duplicate financial charges
- Critical service availability >= 99.9%

These are design targets, not achieved results.
