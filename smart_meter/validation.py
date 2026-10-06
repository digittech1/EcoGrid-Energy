"""Mark a trade verified when accumulated delivery meets its agreed amount."""

def verify_delivery(db, trade_id):
    trade = db.execute("SELECT expected_kwh, status FROM trades WHERE trade_id=?", (trade_id,)).fetchone()
    if trade is None:
        raise ValueError("Unknown trade")
    if trade["status"] in ("VERIFIED", "SETTLED"):
        return True
    delivered = db.execute("SELECT COALESCE(SUM(delivered_kwh),0) FROM meter_readings WHERE trade_id=?", (trade_id,)).fetchone()[0]
    if delivered < trade["expected_kwh"]:
        return False
    with db:
        db.execute("UPDATE trades SET status='VERIFIED' WHERE trade_id=? AND status='PENDING_METER'", (trade_id,))
    return True
