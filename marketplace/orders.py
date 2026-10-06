"""Marketplace: register trades with unique trade IDs."""
import uuid


def create_trade(db, seller_id, buyer_id, expected_kwh, price_per_kwh):
    if not seller_id or not buyer_id or seller_id == buyer_id:
        raise ValueError("Seller and buyer must be different, nonempty IDs")
    if expected_kwh <= 0 or price_per_kwh < 0:
        raise ValueError("Invalid energy amount or price")
    trade_id = str(uuid.uuid4())
    with db:
        db.execute("INSERT INTO trades VALUES (?, ?, ?, ?, ?, ?)",
                   (trade_id, seller_id, buyer_id, expected_kwh, price_per_kwh, "PENDING_METER"))
    return trade_id


def get_trade(db, trade_id):
    row = db.execute("SELECT * FROM trades WHERE trade_id = ?", (trade_id,)).fetchone()
    return dict(row) if row else None
