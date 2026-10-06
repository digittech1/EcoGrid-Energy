import unittest
from shared.database import connect
from marketplace.orders import create_trade
from smart_meter.ingestion import ingest_reading
from smart_meter.validation import verify_delivery
from settlement.transactions import settle_trade


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.db = connect()
        self.trade = create_trade(self.db, "seller", "buyer", 3, 0.2)

    def tearDown(self):
        self.db.close()

    def test_successful_workflow(self):
        self.assertTrue(ingest_reading(self.db, self.trade, "evt1", 3))
        self.assertTrue(verify_delivery(self.db, self.trade))
        self.assertEqual(settle_trade(self.db, self.trade, "key1")["amount"], 0.6)

    def test_duplicate_event(self):
        self.assertTrue(ingest_reading(self.db, self.trade, "evt1", 3))
        self.assertFalse(ingest_reading(self.db, self.trade, "evt1", 3))
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM meter_readings").fetchone()[0], 1)

    def test_settlement_requires_verification(self):
        with self.assertRaises(ValueError):
            settle_trade(self.db, self.trade, "key1")

    def test_idempotent_settlement(self):
        ingest_reading(self.db, self.trade, "evt1", 3)
        verify_delivery(self.db, self.trade)
        first = settle_trade(self.db, self.trade, "key1")
        self.assertEqual(settle_trade(self.db, self.trade, "key1"), first)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM settlements").fetchone()[0], 1)

    def test_conflicting_key_rejected(self):
        ingest_reading(self.db, self.trade, "evt1", 3)
        verify_delivery(self.db, self.trade)
        settle_trade(self.db, self.trade, "key1")
        with self.assertRaises(ValueError):
            settle_trade(self.db, self.trade, "key2")

    def test_insufficient_energy(self):
        ingest_reading(self.db, self.trade, "evt1", 1)
        self.assertFalse(verify_delivery(self.db, self.trade))

    def test_event_collision_rejected(self):
        ingest_reading(self.db, self.trade, "evt1", 1)
        with self.assertRaises(ValueError):
            ingest_reading(self.db, self.trade, "evt1", 2)


if __name__ == "__main__":
    unittest.main()
