"""Atomic local settlement, keyed to trade ID to prevent duplicate charges."""
from settlement.payments import calculate_amount


def settle_trade(db, trade_id, idempotency_key):
    if not idempotency_key:
        raise ValueError("Idempotency key required")
    with db:
        existing = db.execute("SELECT * FROM settlements WHERE trade_id=?", (trade_id,)).fetchone()
        if existing:
            if existing["idempotency_key"] != idempotency_key:
                raise ValueError("Trade already settled using another key")
            return dict(existing)
        trade = db.execute("SELECT * FROM trades WHERE trade_id=?", (trade_id,)).fetchone()
        if trade is None:
            raise ValueError("Unknown trade")
        if trade["status"] != "VERIFIED":
            raise ValueError("Trade requires verified meter delivery")
        amount = calculate_amount(trade["expected_kwh"], trade["price_per_kwh"])
        db.execute("INSERT INTO settlements VALUES (?, ?, ?, ?)",
                   (trade_id, idempotency_key, amount, "COMPLETED"))
        db.execute("UPDATE trades SET status='SETTLED' WHERE trade_id=?", (trade_id,))
    return dict(db.execute("SELECT * FROM settlements WHERE trade_id=?", (trade_id,)).fetchone())
