from decimal import Decimal


def get_exchange_rate():
    exchange_rate = 97.45
    return Decimal.from_float(exchange_rate).quantize(Decimal("1.00"))
