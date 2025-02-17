"""Celery cache backend using the Django Cache Framework."""

from celery.backends.base import KeyValueStoreBackend
from django.core.cache import cache as default_cache
from django.core.cache import caches


class CacheBackend(KeyValueStoreBackend):
    """Backend using the Django cache framework to store task metadata."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Must make sure backend doesn't convert exceptions to dict.
        self.serializer = 'pickle'

    def get(self, key):
        return self.cache_backend.get(key)

    def set(self, key, value):
        self.cache_backend.set(key, value, self.expires)

    def delete(self, key):
        self.cache_backend.delete(key)

    def encode(self, data):
        return data

    def decode(self, data):
        return data

    @property
    def cache_backend(self):
        backend = self.app.conf.cache_backend
        return caches[backend] if backend else default_cache
