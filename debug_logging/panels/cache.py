from debug_toolbar.panels.cache import CacheDebugPanel, CacheStatTracker

from debug_logging.settings import LOGGING_CONFIG


class CacheLoggingPanel(CacheDebugPanel):
    """Extends the Cache debug panel to enable logging."""
    
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
