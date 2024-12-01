from django.core.cache import cache
from common.models import Currency
from common.utils import is_database_synchronized
import logging


LOGGER = logging.getLogger(__name__)


def load_cache():
    if is_database_synchronized("default"):
        LOGGER.debug("Database is not synchronized. Skipping cache loading")
        return
    cache.set("Currency", Currency.objects.all())
    LOGGER.debug("Currency cache set")
