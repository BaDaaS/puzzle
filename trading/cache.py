from django.core.cache import cache
from trading.models import Exchange, Leg, Trade
import logging


LOGGER = logging.getLogger(__name__)

# IMPROVEME.
## - Reset every X seconds
## - Transparent cache, i.e. we could simply use cache.get("Entity") and it would return the Entity objects, not the
## queryset
cache.set("Exchange", Exchange.objects.all())
LOGGER.debug("Exchange cache set")
cache.set("Leg", Leg.objects.all())
LOGGER.debug("Leg cache set")
cache.set("Trade", Trade.objects.all())
LOGGER.debug("Trade cache set")
