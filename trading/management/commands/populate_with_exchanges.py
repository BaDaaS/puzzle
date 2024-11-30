from django.core.management.base import BaseCommand
from trading.models import Exchange
import logging

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        _, created = Exchange.objects.get_or_create(name="Binance")
        if created:
            LOGGER.info("Binance exchange created")
        _, created = Exchange.objects.get_or_create(name="Bitfinex")
        if created:
            LOGGER.info("Bitfinex exchange created")
        _, created = Exchange.objects.get_or_create(name="Coinbase")
        if created:
            LOGGER.info("Coinbase exchange created")
        _, created = Exchange.objects.get_or_create(name="Coinbasepro")
        if created:
            LOGGER.info("Coinbasepro exchange created")
        _, created = Exchange.objects.get_or_create(name="Kraken")
        if created:
            LOGGER.info("Kraken exchange created")
        _, created = Exchange.objects.get_or_create(name="OKex")
        if created:
            LOGGER.info("OKex exchange created")
        _, created = Exchange.objects.get_or_create(name="OKCoin")
        if created:
            LOGGER.info("OKCoin exchange created")
        _, created = Exchange.objects.get_or_create(name="Poloniex")
        if created:
            LOGGER.info("Poloniex exchange created")
