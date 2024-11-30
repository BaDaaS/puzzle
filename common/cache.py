from django.core.cache import cache
from common.models import Currency
import logging


LOGGER = logging.getLogger(__name__)


def load_cache():
    cache.set("Currency", Currency.objects.all())
    LOGGER.debug("Currency cache set")
