"""
Get the balance of an exchange and store it in
InfluxDB and on Redis in a user-specified key.

Usage:
    python manage.py get_exchange_balance \
      --entity=EntityName \
      --measurement=MeasurementName \
      --every=1m \
      --redis-prefix=prefix
"""

from accounting.models import Entity
from common.scheduler import RepeatedTask, parse_schedule
from django.core.management.base import BaseCommand
import logging
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from puzzle.settings import (
    REDIS_HOST,
    REDIS_PORT,
    INFLUXDB_URL,
    INFLUXDB_TOKEN,
    INFLUXDB_ORG,
    INFLUXDB_BUCKET,
)
import redis
from trading.exchange_api.register import REGISTERED_APIS


LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        # FIXME: add an option to raise an exception when there is a new
        # uknown assets
        parser.add_argument("--entity", type=str)
        parser.add_argument("--measurement", type=str)
        parser.add_argument(
            "--every", type=str, help="Frequency of the job", required=True
        )
        parser.add_argument(
            "--redis-prefix",
            type=str,
            required=True,
            help="Prefix for Redis keys",
        )

    def f(self):
        for api in REGISTERED_APIS.iter():
            LOGGER.info(f"Fetching balances for {api.REGISTER_ID}")
            balances = api.get_balance()
            if balances.is_success():
                balances = balances.json()
                for curr, balance in balances.items():
                    balance.entity = self.entity
                    balance.write(
                        write_client=self.write_client,
                        measurement=self.measurement,
                        bucket=INFLUXDB_BUCKET,
                    )
                    balance.set_on_redis(self.redis, self.redis_prefix)

    def handle(self, *args, **kwargs):
        # FIXME: use username, password, etc.
        self.redis = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, decode_responses=True
        )
        self.redis_prefix = kwargs["redis_prefix"]
        self.measurement = kwargs["measurement"]
        self.entity = Entity.objects.get(name=kwargs["entity"])
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
