from django.core.cache import cache
from accounting.models import Entity


# IMPROVEME.
## - Reset every X seconds
## - Transparent cache, i.e. we could simply use cache.get("Entity") and it would return the Entity objects, not the
## queryset
cache.set("Entity", Entity.objects.all())
