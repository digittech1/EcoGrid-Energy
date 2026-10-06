"""Mock payment processor: no bank/payment gateway calls are made."""
from decimal import Decimal, ROUND_HALF_UP


def calculate_amount(kwh, price_per_kwh):
    return float((Decimal(str(kwh)) * Decimal(str(price_per_kwh))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
