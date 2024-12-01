from abc import ABCMeta, abstractmethod
from common.register import AbstractRegister
from common.utils import Price, Quantity, Volume
import json
import requests
from trading.models import Trade
from typing import List


class AbstractReport(metaclass=ABCMeta):
    @abstractmethod
    def make(self) -> List[str]:
        pass


# Trade reports
class AbstractTradeReport(AbstractReport):
    REGISTER_ID = None

    def __init__(self, trade: Trade):
        self.trade = trade


class KrakenTradeReport(AbstractTradeReport):
    REGISTER_ID = "Kraken"

    def make(self) -> List[str]:
        lines = []
        trade_qty = Quantity(self.trade.quantity, self.trade.base_currency)
        trade_price = Price(self.trade.price, self.trade.counter_currency)
        trade_vol = Volume(trade_qty, trade_price)
        lines.append(
            f"Kraken trade: {self.trade.side_str} {trade_qty} at {trade_price} (VOL={trade_vol}) on {self.trade.executed_date}"
        )
        return lines


TRADE_REPORTS = AbstractRegister()
TRADE_REPORTS.register(KrakenTradeReport)


# Reporting platforms
class AbstractReportingPlatform(metaclass=ABCMeta):
    NAME = None
    REGISTER_ID = None

    @abstractmethod
    def post(self):
        pass


class Mattermost(AbstractReportingPlatform):
    REGISTER_ID = "mattermost"

    CONFIGURATION_KEYS = [
        "MATTERMOST_URL",
    ]

    def __init__(self, *args, **kwargs):
        self.url = kwargs["MATTERMOST_URL"]

    def post(self, report: AbstractReport):
        lines = report.make()
        for line in lines:
            data = {"text": line}
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                self.url, data=json.dumps(data), headers=headers
            )
            response.raise_for_status()


class Stdin(AbstractReportingPlatform):
    REGISTER_ID = "stdin"

    CONFIGURATION_KEYS = []

    def post(self, report: AbstractReport):
        lines = report.make()
        for line in lines:
            print(line)


REPORTING_PLATFORMS = AbstractRegister()
REPORTING_PLATFORMS.register(Mattermost)
REPORTING_PLATFORMS.register(Stdin)
