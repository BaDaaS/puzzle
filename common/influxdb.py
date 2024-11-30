from abc import ABCMeta, abstractmethod
from influxdb_client import Point
import logging


LOGGER = logging.getLogger(__name__)


class PublishableData(metaclass=ABCMeta):
    @abstractmethod
    def to_influxdb(self, measurement: str) -> Point:
        pass

    def write(self, write_client, measurement, bucket):
        data = self.to_influxdb(measurement=measurement)
        LOGGER.info(f"Writing data to InfluxDB: {data}")
        write_client.write(bucket=bucket, record=data)
        LOGGER.info("Data written")
