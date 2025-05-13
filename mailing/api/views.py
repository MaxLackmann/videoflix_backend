from django.core.cache.backends.base import DEFAULT_TIMEOUT 
from django.views.decorators.cache import cache_page 
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)