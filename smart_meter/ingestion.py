"""Ingest a unique meter event; repeat delivery is safely ignored."""
import sqlite3


def ingest_reading(db, trade_id, event_id, delivered_kwh):
    if not event_id or delivered_kwh < 0:
        raise ValueError("Invalid meter event")
    if db.execute("SELECT 1 FROM trades WHERE trade_id=?", (trade_id,)).fetchone() is None:
        raise ValueError("Unknown trade")
    try:
        with db:
            db.execute("INSERT INTO meter_readings VALUES (?, ?, ?)",
                       (event_id, trade_id, delivered_kwh))
        return True
    except sqlite3.IntegrityError:
        existing = db.execute("SELECT trade_id, delivered_kwh FROM meter_readings WHERE event_id=?", (event_id,)).fetchone()
        if existing and existing["trade_id"] == trade_id and existing["delivered_kwh"] == delivered_kwh:
            return False
        raise ValueError("Event ID collision with different reading") from None
