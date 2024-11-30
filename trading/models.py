from common.models import Currency
from common.utils import Volume, Price, Quantity
from accounting.models import Entity
from decimal import Decimal
from django.db import models, transaction
from trading.constants import (
    LENGTH_EXCHANGE_NAME,
    LENGTH_INSTRUMENT,
    LENGTH_TRADE_ID,
    TRADE_DECIMAL_PLACES_FEES_QUANTITY,
    TRADE_DECIMAL_PLACES_PRICE,
    TRADE_DECIMAL_PLACES_QUANTITY,
    TRADE_MAX_DIGITS_FEES_QUANTITY,
    TRADE_MAX_DIGITS_PRICE,
    TRADE_MAX_DIGITS_QUANTITY,
)


class Exchange(models.Model):
    name = models.CharField(max_length=LENGTH_EXCHANGE_NAME)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Trade(models.Model):
    SIDE_BUY = 0
    SIDE_SELL = 1

    trade_id = models.CharField(
        max_length=LENGTH_TRADE_ID, unique=True, db_index=True
    )
    quantity = models.DecimalField(
        max_digits=TRADE_MAX_DIGITS_QUANTITY,
        decimal_places=TRADE_DECIMAL_PLACES_QUANTITY,
        null=False,
        blank=False,
    )
    price = models.DecimalField(
        max_digits=TRADE_MAX_DIGITS_PRICE,
        decimal_places=TRADE_DECIMAL_PLACES_PRICE,
        null=False,
        blank=False,
    )
    executed_date = models.DateTimeField()
    side = models.BooleanField()
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    # We authorize more than 6 for futures or for weird name.
    instrument = models.CharField(max_length=LENGTH_INSTRUMENT)
    base_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="base_currencies"
    )
    counter_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="counter_currencies"
    )
    fees_quantity = models.DecimalField(
        max_digits=TRADE_MAX_DIGITS_FEES_QUANTITY,
        decimal_places=TRADE_DECIMAL_PLACES_FEES_QUANTITY,
        null=True,
        blank=True,
    )
    fees_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="fees_currencies",
        null=True,
        blank=True,
    )
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    @property
    def side_str(self):
        if self.side == self.SIDE_BUY:
            return "Buy"
        elif self.side == self.SIDE_SELL:
            return "Sell"
        else:
            raise RuntimeError(
                "Impossible to get the side string for %s" % self.side
            )

    @classmethod
    def get_side_value(cls, v):
        if v.lower() == "buy":
            return cls.SIDE_BUY
        elif v.lower() == "sell":
            return cls.SIDE_SELL
        else:
            raise RuntimeError("Impossible to get the side value for %s" % v)

    def is_buy(self):
        return self.side == self.SIDE_BUY

    def is_sell(self):
        return self.side == self.SIDE_SELL

    def with_fees(self):
        return (
            self.fees_quantity is not None
            and self.fees_quantity != Decimal("0")
            and self.fees_currency is not None
        )

    @property
    def volume(self):
        price = Price(self.price, self.counter_currency)
        qty = Quantity(self.quantity, self.base_currency)
        return Volume(qty=qty, price=price)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        super(Trade, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )
        with transaction.atomic():
            if self.with_fees():
                leg_fees = Leg(
                    trade=self,
                    currency=self.fees_currency,
                    amount=-self.fees_quantity,
                    leg_type=Leg.LEG_TYPE_FEES,
                    exchange=self.exchange,
                )
                leg_fees.save(
                    force_insert=force_insert,
                    force_update=force_update,
                    using=using,
                    update_fields=update_fields,
                )

            if self.is_buy():
                leg_base = Leg(
                    trade=self,
                    currency=self.base_currency,
                    amount=self.quantity,
                    leg_type=Leg.LEG_TYPE_BASE,
                    exchange=self.exchange,
                )
                leg_counter = Leg(
                    trade=self,
                    currency=self.counter_currency,
                    amount=-self.quantity * self.price,
                    leg_type=Leg.LEG_TYPE_COUNTER,
                    exchange=self.exchange,
                )
            else:
                leg_base = Leg(
                    trade=self,
                    currency=self.base_currency,
                    amount=-self.quantity,
                    leg_type=Leg.LEG_TYPE_BASE,
                    exchange=self.exchange,
                )
                leg_counter = Leg(
                    trade=self,
                    currency=self.counter_currency,
                    amount=self.quantity * self.price,
                    leg_type=Leg.LEG_TYPE_COUNTER,
                    exchange=self.exchange,
                )

            leg_base.save(
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields,
            )
            leg_counter.save(
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields,
            )


class Leg(models.Model):
    LEG_TYPE_COUNTER = "Counter"
    LEG_TYPE_BASE = "Base"
    LEG_TYPE_FEES = "Fees"

    LEG_TYPES = [
        (LEG_TYPE_FEES, LEG_TYPE_FEES.upper()),
        (LEG_TYPE_BASE, LEG_TYPE_BASE.upper()),
        (LEG_TYPE_COUNTER, LEG_TYPE_COUNTER.upper()),
    ]

    trade = models.ForeignKey(
        Trade, null=True, blank=True, on_delete=models.CASCADE
    )
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=TRADE_MAX_DIGITS_QUANTITY,
        decimal_places=TRADE_DECIMAL_PLACES_QUANTITY,
    )
    leg_type = models.CharField(max_length=16, choices=LEG_TYPES)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
