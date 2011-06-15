import os.path
import subprocess

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module
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
        if getattr(settings, 'DEBUG_LOGGING_CONFIG', {}).get('ENABLED', False):
            # Logging is enabled, so log the revision
            request.debug_logging_stats.update({
                'revision': self.get_revision()
            })
    
    def get_revision(self):
        vcs = getattr(settings, 'DEBUG_TOOLBAR_CONFIG', {}).get('VCS', None)
        if vcs == 'git':
            module = import_module(settings.SETTINGS_MODULE)
            path = os.path.realpath(os.path.dirname(module.__file__))
            cmd = 'cd %s && git rev-parse --verify --short HEAD' % path
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            proc_stdout, proc_stderr = proc.communicate()
            return proc_stdout
