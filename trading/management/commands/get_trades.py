from decouple import config
from common.reporting_platform import REPORTING_PLATFORMS, TRADE_REPORTS
from common.scheduler import parse_schedule, UnitTask, RepeatedTask
from datetime import timedelta
from datetime import datetime
from django.core.management.base import BaseCommand
from accounting.models import Entity
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
        parser.add_argument("--entity", type=str)
        parser.add_argument("--from-datetime", type=str, required=False)
        parser.add_argument("--until-datetime", type=str, required=False)
        # Examples: 5m, 1h, 30s
        parser.add_argument(
            "--every", type=str, required=False, help="Frequency of the job"
        )

    def f(self):
        from_datetime_dt = self.from_datetime_dt
        until_datetime_dt = self.until_datetime_dt
        exchange = self.exchange
        entity = self.entity
        api = REGISTERED_APIS.get_instance_or_raise(exchange)
        TRADE_REPORT_MAKER = TRADE_REPORTS.get_or_raise(exchange)
        trades = api.get_trades(
            from_datetime=from_datetime_dt, until_datetime=until_datetime_dt
        )
        for trade in trades:
            trade.entity = entity
            # FIXME: this is ugly. Improve me
            if not Trade.objects.filter(trade_id=trade.trade_id).exists():
                LOGGER.info(
                    f"New trade {trade.trade_id} found. Adding to the database and notifying"
                )
                trade_report = TRADE_REPORT_MAKER(trade=trade)
                REPORTING_PLATFORM.post(trade_report)
                trade.save()
            else:
                LOGGER.info(
                    f"Trade {trade.trade_id} already exists in the database. Skipping"
                )
        # Introducing more delay, in case REST API is slow
        self.from_datetime_dt = until_datetime_dt - timedelta(seconds=5)
        self.until_datetime_dt = datetime.now().astimezone()

    def handle(self, *args, **kwargs):
        self.exchange = kwargs["exchange"]
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

        if from_datetime is not None and until_datetime is not None:
            from_datetime_dt = datetime.strptime(
                from_datetime, "%Y-%m-%d-%H-%M-%S"
            ).astimezone()
            until_datetime_dt = datetime.strptime(
                until_datetime, "%Y-%m-%d-%H-%M-%S"
            ).astimezone()
            self.from_datetime_dt = from_datetime_dt
            self.until_datetime_dt = until_datetime_dt
            t = UnitTask(f=self.f)

        elif (
            from_datetime is None or until_datetime is None
        ) and every is None:
            raise ValueError(
                "Either from_datetime and until_datetime or every must be provided"
            )
        else:
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
