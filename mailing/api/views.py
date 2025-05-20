from django.core.cache.backends.base import DEFAULT_TIMEOUT 
from django.views.decorators.cache import cache_page 
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.models import CustomUser



CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)