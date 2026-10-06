"""Run a local end-to-end demo using only synthetic IDs and values."""
from shared.database import connect
from marketplace.orders import create_trade, get_trade
from smart_meter.ingestion import ingest_reading
from smart_meter.validation import verify_delivery
from settlement.transactions import settle_trade


def main():
    db = connect()
    trade_id = create_trade(db, "solar-home-01", "buyer-02", 4.0, 0.25)
    print("Created:", get_trade(db, trade_id)["status"])
    ingest_reading(db, trade_id, "meter-event-001", 4.0)
    print("Verified:", verify_delivery(db, trade_id))
    result = settle_trade(db, trade_id, "payment-key-001")
    print("Settlement:", result["status"], "amount:", result["amount"])
    assert settle_trade(db, trade_id, "payment-key-001") == result
    print("Duplicate settlement safely returned existing record")
    db.close()


if __name__ == "__main__":
    main()
