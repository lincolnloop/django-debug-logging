from django.conf import settings
from debug_toolbar.panels.sql import SQLDebugPanel


class SQLLoggingPanel(SQLDebugPanel):
    """Extends the SQL debug panel to enable logging."""
    
    def process_response(self, request, response):
        if getattr(settings, 'DEBUG_LOGGING_CONFIG', {}).get('ENABLED', False):
            # Logging is enabled, so log the query data
            self._queries = connection.queries[self._offset:]
            self._sql_time = sum([q['duration'] for q in self._queries])
            
            stats = {}
            
            if settings.DEBUG_LOGGING_CONFIG.get('SQL_EXTRA', False):
                stats['sql_queries'] = self._queries
            
            stats['sql_time'] = self._sql_time
            stats['sql_num_queries'] = len(self._queries)
            request.debug_logging_stats.update(stats)
