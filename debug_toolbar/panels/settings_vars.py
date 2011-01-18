from django.conf import settings
from django.template.loader import render_to_string
from django.views.debug import get_safe_settings
from django.utils.translation import ugettext_lazy as _
from debug_toolbar.panels import DebugPanel


class SettingsVarsDebugPanel(DebugPanel):
    """
    A panel to display all variables in django.conf.settings
    """
    name = 'SettingsVars'
    has_content = True

    def nav_title(self):
        return _('Settings')

    def title(self):
        return _('Settings from <code>%s</code>') % settings.SETTINGS_MODULE

    def url(self):
        return ''

    def content(self):
        context = self.context.copy()
        context.update({
            'settings': get_safe_settings(),
        })
        return render_to_string('debug_toolbar/panels/settings_vars.html', context)
    
    def process_response(self, request, response):
        if getattr(settings, 'DEBUG_LOGGING_CONFIG', {}).get('ENABLED', False):
            # Logging is enabled, so log the settings
            stats = {}
            stats['settings'] = get_safe_settings()
            request.debug_logging_stats.update(stats)
