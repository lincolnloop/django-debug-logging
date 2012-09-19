from debug_toolbar.panels.sql import SQLDebugPanel


class SQLLoggingPanel(SQLDebugPanel):
    """Extends the SQL debug panel to enable logging."""
    
    def process_response(self, request, response):
        if getattr(request, 'debug_logging', {}).get('ENABLED', False):
            # Call the nav_subtitle method so that the query data is captured
            self.nav_subtitle()

            for alias, query in self._queries:
                query['alias'] = alias

            stats = {}

            queries = [q for a, q in self._queries]

            if request.debug_logging['SQL_EXTRA']:
                stats['sql_queries'] = queries

            stats['sql_time'] = self._sql_time
            stats['sql_num_queries'] = len(queries)
            request.debug_logging_stats.update(stats)
