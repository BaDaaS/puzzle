from accounting.models import Entity
from common.utils import is_database_synchronized
from django.core.cache import cache
import logging


LOGGER = logging.getLogger(__name__)


def load_cache():
    if is_database_synchronized("default"):
        cache.set("Entity", Entity.objects.all())
        LOGGER.debug("Entity cache set")
    else:
        LOGGER.debug("Database is not synchronized. Skipping cache loading")
