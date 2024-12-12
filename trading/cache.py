from common.utils import is_database_synchronized
from django.core.cache import cache
from trading.models import Exchange, Leg, Trade
import logging


LOGGER = logging.getLogger(__name__)


def load_cache():
    if is_database_synchronized("default"):
        cache.set("Exchange", Exchange.objects.all())
        LOGGER.debug("Exchange cache set")
        cache.set("Leg", Leg.objects.all())
        LOGGER.debug("Leg cache set")
        cache.set("Trade", Trade.objects.all())
        LOGGER.debug("Trade cache set")
    else:
        LOGGER.debug("Database is not synchronized. Skipping cache loading")
