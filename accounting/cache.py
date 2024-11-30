from django.core.cache import cache
from accounting.models import Entity
import logging


LOGGER = logging.getLogger(__name__)


def load_cache():
    cache.set("Entity", Entity.objects.all())
    LOGGER.debug("Entity cache set")
