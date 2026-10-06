"""Illustrative price compatibility check; not a full market-clearing engine."""

def can_match(seller_min_price, buyer_max_price):
    if seller_min_price < 0 or buyer_max_price < 0:
        raise ValueError("Prices cannot be negative")
    return seller_min_price <= buyer_max_price
