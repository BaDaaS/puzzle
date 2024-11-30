"""
This script fetches the price of a list of tickers from an exchange
and writes them to InfluxDB and Redis.

Usage:
    poetry run python manage.py get_price \
      --exchange=exchange_name \
      --tickers=instrument1,instrument2 \
      --every=1m \
      --measurement=measurement_name \
      --redis-prefix=prefix
"""

import redis
from common.scheduler import RepeatedTask, parse_schedule
from django.core.management.base import BaseCommand
from datetime import datetime
from trading.exchange_api.register import REGISTERED_APIS
import logging
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from puzzle.settings import (
    REDIS_HOST,
    REDIS_PORT,
    INFLUXDB_BUCKET,
    INFLUXDB_URL,
    INFLUXDB_TOKEN,
    INFLUXDB_ORG,
)

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--exchange", type=str, required=True)
        parser.add_argument("--tickers", type=str, required=True)
        parser.add_argument(
            "--every", type=str, help="Frequency of the job", required=True
        )
        parser.add_argument(
            "--measurement", type=str, required=True, help="Measurement name"
        )
        parser.add_argument(
            "--redis-prefix",
            type=str,
            required=True,
            help="Prefix for Redis keys",
        )

    def f(self):
        now = datetime.now().astimezone()
        LOGGER.info(
            f"Fetching tickers for {self.exchange} at {now}, instruments: {self.tickers}"
        )
        prices = self.api.get_tickers(self.tickers)
        LOGGER.info(f"Prices for {self.exchange} at {now}:")
        for ticker, price in prices.items():
            price.write(
                self.write_client,
                measurement=self.measurement,
                bucket=INFLUXDB_BUCKET,
            )
            price.set_on_redis(self.redis, self.redis_prefix)

    def handle(self, *args, **kwargs):
        self.redis_prefix = kwargs["redis_prefix"]
        self.redis = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, decode_responses=True
        )
        self.exchange = kwargs["exchange"]
        self.measurement = kwargs["measurement"]
        self.tickers = kwargs["tickers"].split(",")
        self.api = REGISTERED_APIS.get_instance_or_raise(self.exchange)
        # FIXME: organize in a different file to unify the logic
        self.client = InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG,
            verify_ssl=False,
        )
        self.write_client = self.client.write_api(write_options=SYNCHRONOUS)
        every = kwargs["every"]

        every, unit = parse_schedule(every)
        every = {
            "s": every,
            "m": every * 60,
            "h": every * 60 * 60,
        }[unit]

        t = RepeatedTask(self.f, every_sec=every)
        t.run()
