from accounting.models import Entity
from common.influxdb import PublishableData as PublishableInfluxData
from common.models import Currency
from decimal import Decimal
from influxdb_client import Point
from typing import Optional


class AbstractBalance(PublishableInfluxData):
    def __init__(
        self,
        d: Decimal,
        c: Currency,
        timestamp_utc_ns: int,
        source: str,
        entity: Optional[Entity],
    ):
        assert isinstance(d, Decimal)
        assert isinstance(c, Currency)
        assert isinstance(timestamp_utc_ns, int)
        assert isinstance(source, str)
        assert isinstance(entity, Entity) or entity is None
        self.d = d
        self.c = c
        self.entity = entity
        self.timestamp_utc_ns = timestamp_utc_ns
        self.source = source

    def to_influxdb(self, measurement):
        """
        Tags:
        - currency: currency symbol
        - entity: entity name
        - source: source of the balance

        Fields:
        - balance: balance
        """
        balance_float = float(self.d)
        # We force to have an entity
        assert self.entity is not None
        return (
            Point(measurement)
            .tag("currency", self.c.symbol)
            .tag("entity", self.entity.name)
            .tag("source", self.source)
            .field("balance", balance_float)
            .time(self.timestamp_utc_ns)
        )

    def set_on_redis(self, redis_client, prefix_key: str) -> bool:
        key = f"{prefix_key}/{self.source}-{self.entity.name}"
        j = {
            "p": str(self.d),
            "c": self.c.symbol,
            "t": self.timestamp_utc_ns,
            "s": self.source,
            "e": self.entity.name,
        }
        return redis_client.hset(key, mapping=j)

    @classmethod
    def from_redis(
        cls, redis_client, prefix_key: str, source: str, entity: Entity
    ):
        key = f"{prefix_key}/{source}-{entity.name}"
        res = redis_client.hgetall(key)
        if res is not None:
            entity = Entity.objects.get(name=res["e"])
            currency = Currency.objects.get(symbol=res["c"])
            return AbstractBalance(
                d=Decimal(res["p"]),
                c=currency,
                timestamp_utc_ns=int(res["t"]),
                source=res["s"],
                entity=entity,
            )
        return None


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
    supported_decimals = {2, 6, 8, 9, 18}
    if currency.decimals in supported_decimals:
        return f"{currency.symbol}{amount:,.{currency.decimals}f}"
    
    print(f"FIXME: decimals not implemented for currency {currency.symbol}")
    return f"{currency.symbol}{amount:,f}"


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
