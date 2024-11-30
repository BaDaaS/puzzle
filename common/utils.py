from common.models import Currency
from decimal import Decimal


class Price:
    def __init__(self, d: Decimal, c: Currency):
        self.d = d
        self.c = c

    def __str__(self):
        return "{}{:,f}".format(self.c.symbol, self.d)

    def __repr__(self):
        return self.__str__()

    def __format__(self, *args, **kwars):
        return self.__str__()


class Quantity:
    """
    A quantity is a number of items, in our case a currency.
    """

    def __init__(self, d: Decimal, c: Currency):
        self.d = d
        self.c = c

    def __str__(self):
        return "{}{:,f}".format(self.c.symbol, self.d)

    def __repr__(self):
        return self.__str__()

    def __format__(self, *args, **kwars):
        return self.__str__()


def str_amount_based_on_currency(amount: Decimal, currency: Currency) -> str:
    if currency.decimals == 2:
        return "{}{:,.2f}".format(currency.symbol, amount)
    elif currency.decimals == 6:
        return "{}{:,.6f}".format(currency.symbol, amount)
    elif currency.decimals == 8:
        return "{}{:,.8f}".format(currency.symbol, amount)
    elif currency.decimals == 9:
        return "{}{:,.9f}".format(currency.symbol, amount)
    elif currency.decimals == 18:
        return "{}{:,.18f}".format(currency.symbol, amount)
    else:
        print(
            "FIXME: decimals not implemented for currency {}".format(
                currency.symbol
            )
        )
        return "{}{:,f}".format(currency.symbol, amount)


class Volume:
    """
    The volume is the amount of values traded.
    It is the product of a quantity at a certain price.
    The unit is the price unit.
    """

    def __init__(self, qty: Quantity, price: Price):
        self.qty = qty
        self.price = price
        self.value = qty.d * price.d
        self.currency = price.c

    def __str__(self):
        return str_amount_based_on_currency(self.value, self.currency)
