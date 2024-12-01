from accounting.models import Entity
from common.http_helpers import AbstractResponse, SuccessResponse, ErrorResponse
from common.models import Currency
from common.utils import AbstractBalance
from ccxt.base.errors import (
    InvalidNonce,
    RequestTimeout,
    ExchangeNotAvailable,
    NetworkError,
)
from datetime import datetime
from dateutil.parser import parse
from decimal import Decimal
from django.conf import settings
from django.core.cache import cache
import logging
import time
from trading.exchange_api.base import AbstractAPI
from trading.models import Trade
from trading.utils import FIATDeposit
from typing import List


LOGGER = logging.getLogger(__name__)
CacheCurrency = cache.get("Currency")
CacheAccount = cache.get("Account")
CacheEntity = cache.get("Entity")


class API(AbstractAPI):
    REGISTER_ID = "Kraken"
    EXCHANGE_CCXT_NAME = "kraken"

    CURRENCY_MAPPING = {
        # Normal mapping
        "BTC": CacheCurrency.get(symbol="BTC"),
        "USD": CacheCurrency.get(symbol="USD"),
        "GBP": CacheCurrency.get(symbol="GBP"),
        "EUR": CacheCurrency.get(symbol="EUR"),
        "ETH": CacheCurrency.get(symbol="ETH"),
        "ZEC": CacheCurrency.get(symbol="ZEC"),
        "XMR": CacheCurrency.get(symbol="XMR"),
        "OP": CacheCurrency.get(symbol="OP"),
        "AAVE": CacheCurrency.get(symbol="AAVE"),
        "ALGO": CacheCurrency.get(symbol="ALGO"),
        "MINA": CacheCurrency.get(symbol="MINA"),
        "USDT": CacheCurrency.get(symbol="USDT"),
        "DOT": CacheCurrency.get(symbol="DOT"),
        "AVAX": CacheCurrency.get(symbol="AVAX"),
        "USDC": CacheCurrency.get(symbol="USDC"),
        "XTZ": CacheCurrency.get(symbol="XTZ"),
        "LUNA": CacheCurrency.get(symbol="LUNA"),
        "SOL": CacheCurrency.get(symbol="SOL"),
        "SAND": CacheCurrency.get(symbol="SAND"),
        "AXS": CacheCurrency.get(symbol="AXS"),
        "BCH": CacheCurrency.get(symbol="BCH"),
        "BSV": CacheCurrency.get(symbol="BSV"),
        "CRV": CacheCurrency.get(symbol="CRV"),
        # Kraken specifics
        "ETH2.S": CacheCurrency.get(symbol="ETH.S"),
        "MINA.S": CacheCurrency.get(symbol="MINA.S"),
        # Seems to be spot
        "MINA.F": CacheCurrency.get(symbol="MINA"),
        "SOL.S": CacheCurrency.get(symbol="SOL.S"),
        "EUR.M": CacheCurrency.get(symbol="EUR"),
        "DOT.S": CacheCurrency.get(symbol="DOT.S"),
        "XETH": CacheCurrency.get(symbol="ETH"),
        "XXBT": CacheCurrency.get(symbol="BTC"),
        "XZEC": CacheCurrency.get(symbol="ZEC"),
        "XTZ.S": CacheCurrency.get(symbol="XTZ.S"),
        "XXMR": CacheCurrency.get(symbol="XMR"),
        "XXLM": CacheCurrency.get(symbol="XLM"),
        "LUNA2": CacheCurrency.get(symbol="LUNA2"),
        "XXRP": CacheCurrency.get(symbol="XRP"),
        "ZEUR": CacheCurrency.get(symbol="EUR"),
        # Kraken on 20240601
        # Seems to be because I activated rewards the week before.
        # We're getting some %. 0.10% on BTC.
        # Classifying them as the same ticker.
        "XBT.F": CacheCurrency.get(symbol="BTC"),
        "ETH.F": CacheCurrency.get(symbol="ETH"),
    }

    def __init__(
        self,
        api_key: str = settings.CRYPTO_EXCHANGE_KRAKEN_API_KEY,
        secret_key: str = settings.CRYPTO_EXCHANGE_KRAKEN_SECRET_KEY,
    ):
        for key, value in self.CURRENCY_MAPPING.items():
            assert isinstance(
                value, Currency
            ), f"{key} is not a Currency object"

        super(API, self).__init__(api_key=api_key, secret_key=secret_key)

    def parse_raw_trade(self, trade) -> Trade:
        trade_id = trade["id"]
        executed_date = parse(trade["datetime"])
        quantity = Decimal(str(trade["amount"]))
        price = Decimal(str(trade["price"]))
        side = Trade.get_side_value(trade["side"])
        instrument = trade["symbol"]
        raw_base_currency, raw_counter_currency = instrument.split("/")
        base_currency = self.CURRENCY_MAPPING[raw_base_currency]
        counter_currency = self.CURRENCY_MAPPING[raw_counter_currency]
        fees_quantity = Decimal(str(trade["fee"]["cost"]))
        raw_fees_currency = trade["fee"]["currency"]
        fees_currency = self.CURRENCY_MAPPING[raw_fees_currency]
        obj = Trade(
            trade_id=trade_id,
            quantity=quantity,
            price=price,
            executed_date=executed_date,
            side=side,
            exchange=self.exchange,
            instrument=instrument,
            base_currency=base_currency,
            counter_currency=counter_currency,
            fees_quantity=fees_quantity,
            fees_currency=fees_currency,
        )
        return obj

    def get_trades(
        self, from_datetime: datetime, until_datetime: datetime
    ) -> List[Trade]:
        # Kraken API uses milliseconds
        LOGGER.info(
            f"Fetching trades from {from_datetime} to {until_datetime} using pagination"
        )
        trades = []
        last_trade_date = from_datetime
        last_trade_id = None
        while last_trade_date < until_datetime:
            LOGGER.info(f"Fetching trades since {last_trade_date}")
            # We process each trade
            # update the last trade date with the
            # most recent one in the list received from the
            # API, and we get the next page of trades using
            # the last trade date as a starting point,
            # until we reach the until_datetime or we run out of trades.
            # Might be a weird way to parse, but we never
            # know if the API will return the trades in the correct order or correctly
            last_trade_datetime_ms = int(last_trade_date.timestamp() * 1000)
            # Limit must be at last 2 for the pagination to work
            try:
                raw_trades = self.api.fetch_my_trades(
                    since=last_trade_datetime_ms, limit=100
                )
            except InvalidNonce as e:
                LOGGER.error(f"Invalid nonce: {e}. Retrying in 1 second")
                time.sleep(1)
                return self.get_trades(from_datetime, until_datetime)
            except RequestTimeout as e:
                LOGGER.error(f"Request timeout: {e}. Retrying in 1 second")
                time.sleep(1)
                return self.get_trades(from_datetime, until_datetime)
            except NetworkError as e:
                LOGGER.error(f"Network error: {e}. Retrying in 1 second")
                time.sleep(1)
                return self.get_trades(from_datetime, until_datetime)
            except Exception as e:
                LOGGER.error("Exception not handled: {e}. Stopping")
                raise e

            # Last trade info
            LOGGER.info(f"Found {len(raw_trades)} trades. Parsing each")
            if len(raw_trades) == 0:
                return trades
            for trade in raw_trades:
                trade_id = trade["id"]
                # If we reached this condition, we know we have reached
                # the last trade, and the last trade has been executed.
                # We also suppose that two trades can't happen at the exact same time
                if len(raw_trades) == 1 and trade_id == last_trade_id:
                    LOGGER.info(f"Reached last trade {trade_id}, stopping")
                    return trades
                executed_date = parse(trade["datetime"])
                # Sanity check in case fetch_my_trades returns a trade out of the range
                if from_datetime <= executed_date <= until_datetime:
                    trade = self.parse_raw_trade(trade)
                    LOGGER.info(f"Adding trade {trade_id} to the list")
                    trades.append(trade)
                else:
                    LOGGER.info(
                        f"Trade {trade_id} is out of the date range ({executed_date}), skipping"
                    )
                # Even if the trade is out of the range, we still update the
                # last trade date if it's more recent, it is
                # a way to stop the pagination
                if last_trade_date is None or executed_date > last_trade_date:
                    LOGGER.info(
                        f"Updating last trade date from {last_trade_date} to {executed_date}"
                    )
                    last_trade_date = executed_date
                    last_trade_id = trade_id
        return trades

    def get_balance(self) -> AbstractResponse:
        try:
            result = self.api.fetch_balance()
        except InvalidNonce as e:
            LOGGER.error(f"Invalid nonce: {e}. Retrying in 1 second")
            time.sleep(1)
            return self.get_balance()
        except RequestTimeout as e:
            LOGGER.error(f"Request timeout: {e}. Retrying in 1 second")
            time.sleep(1)
            return self.get_balance()
        except NetworkError as e:
            LOGGER.error(f"Network error: {e}. Retrying in 1 second")
            time.sleep(1)
            return self.get_balance()
        except ExchangeNotAvailable as e:
            LOGGER.error(f"Exchange not available: {e}. Retrying in 1 second")
            time.sleep(1)
            return self.get_balance()
        except Exception as e:
            LOGGER.error(f"Exception not handled: {e}. Stopping")
            raise e
        result_info = result["info"]
        if result_info["error"] != []:
            return ErrorResponse(
                response=result, response_json=result_info["error"]
            )
        raw_balances = result_info["result"]
        balances = {}
        for curr, raw_balance in raw_balances.items():
            amount = Decimal(raw_balance["balance"])
            internal_curr = self.CURRENCY_MAPPING.get(curr)
            if internal_curr is None:
                LOGGER.warn(
                    "IGNORING {} as there is no mapping. The balance is {}".format(
                        curr, amount
                    )
                )
            else:
                # We gather different ticker that are representing the same risk, for now.
                if internal_curr in balances:
                    balances[internal_curr].d += amount
                else:
                    # Info to build an AbstractBalance object
                    now = datetime.now().astimezone()
                    timestamp_utc_ns = int(now.timestamp() * 1_000_000_000)
                    source = self.REGISTER_ID.lower()
                    balance = AbstractBalance(
                        c=internal_curr,
                        d=amount,
                        timestamp_utc_ns=timestamp_utc_ns,
                        source=source,
                        # Will be set later
                        entity=None,
                    )
                    balances[internal_curr] = balance
            # currency
        return SuccessResponse(
            response=result, response_json=balances, status_code=200
        )

    def get_fiat_deposits(
        self,
        from_datetime: datetime,
        until_datetime: datetime,
        entity: Entity,
        currency: Currency,
    ) -> List[FIATDeposit]:
        raise ValueError("Unimplemented")
