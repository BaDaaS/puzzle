from abc import ABCMeta, abstractmethod
from accounting.models import Entity
from base.utils import TickPrice
import ccxt
from ccxt.base.errors import (
    RequestTimeout,
    NetworkError,
)
from common.http_helpers import AbstractResponse
from common.models import Currency
from datetime import datetime, timezone
from decimal import Decimal
import logging
import time
from trading.models import Trade, Exchange
from typing import List


LOGGER = logging.getLogger(__name__)


class AbstractAPI(metaclass=ABCMeta):
    EXCHANGE_CCXT_NAME = None
    CURRENCY_MAPPING = {}

    def __init__(self, api_key: str, secret_key: str):
        assert (
            self.EXCHANGE_CCXT_NAME is not None
        ), "EXCHANGE_CCXT_NAME must be set for the API"
        assert api_key is not None, "API key must be set for the API"
        assert secret_key is not None, "Secret key must be set for the API"
        self.exchange = Exchange.objects.get(name=self.REGISTER_ID)
        self.api_key = api_key
        self.secret_key = secret_key
        self.api = getattr(ccxt, self.EXCHANGE_CCXT_NAME)(
            {"apiKey": self.api_key, "secret": self.secret_key}
        )

    @abstractmethod
    def get_trades(
        self, from_datetime: datetime, until_datetime: datetime
    ) -> List[Trade]:
        pass

    @abstractmethod
    def get_balance(self) -> AbstractResponse:
        pass

    def get_tickers(self, instrument: List[str]):
        """
        Fetches the tickers for the specified instruments.
        :param instrument: List of instrument symbols.
        :return: List of tickers.

        Could be specialized for each exchange.
        """
        LOGGER.info(f"Fetching tickers for {instrument}")
        try:
            res = self.api.fetch_tickers(instrument)
        except RequestTimeout as e:
            LOGGER.error(f"Request timeout: {e}. Retrying in 1 second")
            time.sleep(1)
            return self.get_tickers(instrument=instrument)
        except NetworkError as e:
            LOGGER.error(f"Network error: {e}. Retrying in 1 second")
            time.sleep(1)
            return self.get_tickers(instrument=instrument)
        prices = {}
        for instr, d in res.items():
            base_currency, counter_currency = instr.split("/")
            base_currency = self.CURRENCY_MAPPING[base_currency]
            counter_currency = self.CURRENCY_MAPPING[counter_currency]
            mid_decimal = Decimal(str(d["average"]))
            # FIXME: use time.time_ns(). be careful with the timezone.
            timestamp_utc_ns = int(
                datetime.now(timezone.utc).timestamp() * 1000_000_000
            )
            exchange_name = self.exchange.name.lower()
            tick_price = TickPrice(
                instrument=instr,
                price=mid_decimal,
                exchange=exchange_name,
                timestamp_utc_ns=timestamp_utc_ns,
                counter_currency=counter_currency,
                base_currency=base_currency,
            )
            prices[instr] = tick_price
        return prices

    @abstractmethod
    def get_fiat_deposits(
        self,
        from_datetime: datetime,
        until_datetime: datetime,
        entity: Entity,
        currency: Currency,
    ):
        pass
