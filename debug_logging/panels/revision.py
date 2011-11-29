from django.utils.translation import ugettext_lazy as _
from debug_logging.utils import get_revision
from debug_toolbar.panels import DebugPanel


class RevisionLoggingPanel(DebugPanel):
    """
    A panel to display the current source code revision. Currently only
    supports git.
    """
    name = 'Revision'
    has_content = False

    def nav_title(self):
        return _('Revision')

    def nav_subtitle(self):
        return self.get_revision() or 'Revision unavailable'

    def process_response(self, request, response):
        if getattr(request, 'debug_logging', {}).get('ENABLED', False):
            # Logging is enabled, so log the revision
            request.debug_logging_stats.update({
                'revision': self.get_revision()
            })

    def get_revision(self):
        return get_revision()
