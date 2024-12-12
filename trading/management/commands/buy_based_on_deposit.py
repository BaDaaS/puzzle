from decouple import config
from common.reporting_platform import REPORTING_PLATFORMS, TRADE_REPORTS
from common.scheduler import parse_schedule, UnitTask, RepeatedTask
from datetime import timedelta
from datetime import datetime
from django.core.management.base import BaseCommand
from accounting.models import Entity
from common.models import Currency
from trading.models import Trade
from trading.exchange_api.register import REGISTERED_APIS
import logging

LOGGER = logging.getLogger(__name__)

# Config reporting platform
REPORTING_PLATFORM_NAME = config("REPORTING_PLATFORM_NAME")
REPORTING_PLATFORM = REPORTING_PLATFORMS.get_or_raise(REPORTING_PLATFORM_NAME)
REPORTING_PLATFORM_CONFIG = {
    k: config(k) for k in REPORTING_PLATFORM.CONFIGURATION_KEYS
}
REPORTING_PLATFORM = REPORTING_PLATFORM(**REPORTING_PLATFORM_CONFIG)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--exchange", type=str)
        parser.add_argument(
            "--currency",
            type=str,
            help="Currency of deposits to trigger trade from",
        )
        parser.add_argument("--entity", type=str)
        # Examples: 5m, 1h, 30s
        parser.add_argument(
            "--every", type=str, required=False, help="Frequency of the job"
        )

    def f(self):
        api = REGISTERED_APIS.get_instance_or_raise(self.exchange)
        TRADE_REPORT_MAKER = TRADE_REPORTS.get_or_raise(self.exchange)
        deposits = api.get_fiat_deposits(
            from_datetime=self.from_datetime_dt,
            until_datetime=self.until_datetime_dt,
            entity=self.entity,
            currency=self.currency,
        )
        for deposit in deposits:
            print(deposit)
        self.from_datetime_dt = self.until_datetime_dt - timedelta(seconds=5)
        self.until_datetime_dt = datetime.now().astimezone()

    def handle(self, *args, **kwargs):
        self.exchange = kwargs["exchange"]
        currency = kwargs["currency"]
        self.currency = Currency.objects.get(symbol=currency)
        entity = kwargs["entity"]
        self.entity = Entity.objects.get(name=entity)

        # Timing parsing. IMPROVEME. This is a bit messy, we should
        # move it to an appropriate scheduler implementation
        # If every is provided, we will use it to schedule the job
        # Otherwise, we will use from_datetime and until_datetime to
        # fetch the transactions only once
        from_datetime = kwargs.get("from_datetime", None)
        until_datetime = kwargs.get("until_datetime", None)
        every = kwargs.get("every", None)

        every, unit = parse_schedule(every)
        self.every = {
            "s": every,
            "m": every * 60,
            "h": every * 60 * 60,
        }[unit]
        now = datetime.now().astimezone()
        # Introducing more delay, in case REST API is slow
        self.from_datetime_dt = now - timedelta(seconds=10)
        self.until_datetime_dt = now
        t = RepeatedTask(f=self.f, every_sec=self.every)

        t.run()
