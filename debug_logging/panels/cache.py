# This import can be removed once the workaround below goes into a release
from django.core import cache
from debug_toolbar.panels.cache import CacheDebugPanel, CacheStatTracker

from debug_logging.settings import LOGGING_CONFIG


class CacheLoggingPanel(CacheDebugPanel):
    """Extends the Cache debug panel to enable logging."""

    def __init__(self, *args, **kwargs):
        """
        This method is copied & pasted from SQLDebugPanel to overcome the issue
        described here:

        https://github.com/django-debug-toolbar/django-debug-toolbar/pull/178

        Once this issue is closed and the pull request is merged, this __init__
        method can be entirely removed.
        """
        self.context.update(kwargs.get('context', {}))
        # This is hackish but to prevent threading issues is somewhat needed
        if isinstance(cache.cache, CacheStatTracker):
            cache.cache.reset()
            self.cache = cache.cache
        else:
            self.cache = CacheStatTracker(cache.cache)
            cache.cache = self.cache

    def process_response(self, request, response):
        if getattr(request, 'debug_logging', {}).get('ENABLED', False):
            # Logging is enabled, so log the cache data

            stats = {}

            stats['cache_num_calls'] = len(self.cache.calls)
            stats['cache_time'] = self.cache.total_time
            stats['cache_hits'] = self.cache.hits
            stats['cache_misses'] = self.cache.misses
            stats['cache_sets'] = self.cache.sets
            stats['cache_gets'] = self.cache.gets
            stats['cache_get_many'] = self.cache.get_many
            stats['cache_deletes'] = self.cache.deletes

            if LOGGING_CONFIG['CACHE_EXTRA']:
                stats['cache_calls'] = self.cache.calls

            request.debug_logging_stats.update(stats)
