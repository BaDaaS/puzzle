from django.core.cache import cache
from trading.models import Exchange, Leg, Trade


# IMPROVEME.
## - Reset every X seconds
## - Transparent cache, i.e. we could simply use cache.get("Entity") and it would return the Entity objects, not the
## queryset
cache.set("Exchange", Exchange.objects.all())
cache.set("Leg", Leg.objects.all())
cache.set("Trade", Trade.objects.all())
