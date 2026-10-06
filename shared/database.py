"""SQLite persistence for a single-process demonstration (not distributed storage)."""
import sqlite3


def connect(path=":memory:"):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript("""
    CREATE TABLE IF NOT EXISTS trades (
        trade_id TEXT PRIMARY KEY,
        seller_id TEXT NOT NULL,
        buyer_id TEXT NOT NULL,
        expected_kwh REAL NOT NULL CHECK(expected_kwh > 0),
        price_per_kwh REAL NOT NULL CHECK(price_per_kwh >= 0),
        status TEXT NOT NULL CHECK(status IN ('PENDING_METER','VERIFIED','SETTLED'))
    );
    CREATE TABLE IF NOT EXISTS meter_readings (
        event_id TEXT PRIMARY KEY,
        trade_id TEXT NOT NULL REFERENCES trades(trade_id),
        delivered_kwh REAL NOT NULL CHECK(delivered_kwh >= 0)
    );
    CREATE TABLE IF NOT EXISTS settlements (
        trade_id TEXT PRIMARY KEY REFERENCES trades(trade_id),
        idempotency_key TEXT NOT NULL UNIQUE,
        amount REAL NOT NULL CHECK(amount >= 0),
        status TEXT NOT NULL CHECK(status = 'COMPLETED')
    );
    """)
    return connection
