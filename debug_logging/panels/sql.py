from django.db.backends import BaseDatabaseWrapper
from debug_toolbar.panels.sql import SQLDebugPanel
from debug_toolbar.middleware import DebugToolbarMiddleware
from debug_toolbar.utils.tracking import replace_call


# Warning, ugly hackery ahead. Place an alias to the logging class in the
# panels dict.
@replace_call(BaseDatabaseWrapper.cursor)
def cursor(func, self):
    djdt = DebugToolbarMiddleware.get_current()
    if djdt:
        djdt._panels[SQLDebugPanel] = djdt.get_panel(SQLLoggingPanel)
    return func(self)


class SQLLoggingPanel(SQLDebugPanel):
    """Extends the SQL debug panel to enable logging."""

    def process_response(self, request, response):
        super(SQLLoggingPanel, self).process_response(request, response)
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
