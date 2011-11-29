import logging

from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch

from debug_toolbar.toolbar.loader import DebugToolbar
from debug_toolbar.middleware import DebugToolbarMiddleware
from debug_logging.settings import LOGGING_CONFIG

logger = logging.getLogger('debug.logger')
for HandlerClass in LOGGING_CONFIG["LOGGING_HANDLERS"]:
    logger.addHandler(HandlerClass)


class DebugLoggingMiddleware(DebugToolbarMiddleware):
    """
    Extends the Debug Toolbar middleware with some extras for logging stats.
    """

    def _logging_enabled(self, request):
        return request.META.get('DJANGO_DEBUG_LOGGING', False)

    def _show_toolbar(self, request):
        if self._logging_enabled(request):
            # If logging is enabled, don't show the toolbar
            return False
        return super(DebugLoggingMiddleware, self)._show_toolbar(request)

    def process_request(self, request):
        if self._logging_enabled(request):
            request.debug_logging = LOGGING_CONFIG
            request.debug_logging['ENABLED'] = True
        response = super(DebugLoggingMiddleware, self).process_request(request)

        if self._logging_enabled(request):
            # If the debug-logging frontend is in use, add it to the blacklist
            blacklist = request.debug_logging['BLACKLIST']
            try:
                debug_logging_prefix = reverse('debug_logging_index')
                blacklist.append(debug_logging_prefix)
            except NoReverseMatch:
                pass

            # Don't log requests to urls in the blacklist
            for blacklist_url in blacklist:
                if request.path.startswith(blacklist_url):
                    return response

            # Add an attribute to the request to track stats, and log the
            # request path
            request.debug_logging_stats = {'request_path': request.path}

            self.debug_toolbars[request] = DebugToolbar(request)
            for panel in self.debug_toolbars[request].panels:
                panel.process_request(request)

        return response

    def process_response(self, request, response):
        response = super(DebugLoggingMiddleware, self).process_response(
            request, response)

        if response.status_code == 200:
            if self._logging_enabled(request) and \
              hasattr(request, 'debug_logging_stats'):
                # If logging is enabled, log the stats to the selected handler
                logger.debug(request.debug_logging_stats)

        return response
