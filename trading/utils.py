from accounts.models import Account, Entity
from common.models import Currency
from datetime import datetime
from decimal import Decimal
from common.influxdb import PublishableData as PublishableInfluxData
from influxdb_client import Point
from typing import Optional


class FIATDeposit:
    def __init__(
        self,
        currency: Currency,
        amount: Decimal,
        executed_date: datetime,
        sender: Account,
        receiver: str,
        entity: Optional[Entity],
        txid: str,
    ):
        self.txid = txid
        self.currency = currency
        self.amount = amount
        self.executed_date = executed_date
        self.sender = sender
        self.receiver = receiver
        self.entity = entity


class TickPrice(PublishableInfluxData):
    def __init__(
        self,
        instrument: str,
        price: Decimal,
        exchange: str,
        timestamp_utc_ns: int,
        counter_currency: Currency,
        base_currency: Currency,
    ):
        assert isinstance(instrument, str)
        assert isinstance(price, Decimal)
        assert isinstance(exchange, str)
        assert isinstance(timestamp_utc_ns, int)
        assert isinstance(counter_currency, Currency)
        assert isinstance(base_currency, Currency)

        self.instrument = instrument
        self.price = price
        self.exchange = exchange
        self.timestamp_utc_ns = timestamp_utc_ns
        self.counter_currency = counter_currency
        self.base_currency = base_currency

    def to_influxdb(self, measurement):
        """
        Tags:
        - counter_currency: counter currency symbol
        - base_currency: base currency symbol
        - instrument: instrument
        - exchange: exchange
        Fields:
        - price: price
        """
        return (
            Point(measurement)
            .tag("counter_currency", self.counter_currency.symbol)
            .tag("base_currency", self.base_currency.symbol)
            .tag("instrument", self.instrument)
            .tag("exchange", self.exchange)
            .field("price", float(self.price))
            .time(self.timestamp_utc_ns)
        )

    def set_on_redis(self, redis_client, prefix_key: str):
        key = f"{prefix_key}/{self.exchange}/{self.instrument}"
        j = {
            "c": self.counter_currency.symbol,
            "b": self.base_currency.symbol,
            "i": self.instrument,
            "t": self.timestamp_utc_ns,
            "e": self.exchange,
            "p": str(self.price),
        }
        return redis_client.hset(key, mapping=j)
