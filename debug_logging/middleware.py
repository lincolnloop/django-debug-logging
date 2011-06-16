import logging

from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch

from debug_toolbar.toolbar.loader import DebugToolbar
from debug_toolbar.middleware import DebugToolbarMiddleware
from debug_logging.handlers import DBHandler

logger = logging.getLogger('debug.logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(DBHandler())


class DebugLoggingMiddleware(DebugToolbarMiddleware):
    """
    Extends the Debug Toolbar middleware with some extras for logging stats.
    """
    
    def __init__(self):
        super(DebugLoggingMiddleware, self).__init__()
        
        # Determine whether logging is enabled
        self.logging_enabled = False
        if hasattr(settings, 'DEBUG_LOGGING_CONFIG'):
            if settings.DEBUG_LOGGING_CONFIG.get('ENABLED', False):
                self.logging_enabled = True

    def _show_toolbar(self, request):
        if self.logging_enabled:
            # If logging is enabled, don't show the toolbar
            return False
        return super(DebugLoggingMiddleware, self)._show_toolbar(request)
    
    def process_request(self, request):
        response = super(DebugLoggingMiddleware, self).process_request(request)
        
        # If the debug-logging frontend is in use, don't log requests to the UI
        try:
            debug_logging_prefix = reverse('debug-logging:index')
            if debug_logging_prefix in request.path:
                return
        except NoReverseMatch:
            pass
        
        if self.logging_enabled:
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
            if self.logging_enabled and hasattr(request, 'debug_logging_stats'):
                # If logging is enabled, log the stats to the selected handler                
                logger.debug(request.debug_logging_stats)
        
        return response
