from django.utils.translation import ugettext_lazy as _

from debug_logging.utils import get_project_name, get_hostname
from debug_toolbar.panels import DebugPanel


class IdentityLoggingPanel(DebugPanel):
    """
    A panel to display the current site name and hostname, to identify the
    current environment for logging.
    """
    name = 'Identity'
    has_content = False

    def nav_title(self):
        return _('Identity')

    def nav_subtitle(self):
        project_name, hostname = self.identify()
        if project_name and hostname:
            return '%s on %s' % (project_name, hostname)

    def process_response(self, request, response):
        if getattr(request, 'debug_logging', {}).get('ENABLED', False):
            project_name, hostname = self.identify()
            # Logging is enabled, so log the revision
            request.debug_logging_stats.update({
                'project_name': project_name,
                'hostname': hostname,
            })

    def identify(self):
        return get_project_name(), get_hostname()
