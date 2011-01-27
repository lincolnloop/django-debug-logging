import re

from django.conf import settings
from django.template.loader import render_to_string
from django.views.debug import get_safe_settings
from django.utils.translation import ugettext_lazy as _
from debug_toolbar.panels import DebugPanel

LOGGED_SETTINGS = re.compile(
    'CACHE_BACKEND|CACHE_MIDDLEWARE_KEY_PREFIX|CACHE_MIDDLEWARE_SECONDS|' +
    'DATABASES|DEBUG|DEBUG_LOGGING_CONFIG|DEBUG_TOOLBAR_CONFIG|' +
    'DEBUG_TOOLBAR_PANELS|INSTALLED_APPS|INTERNAL_IPS|MIDDLEWARE_CLASSES|' +
    'TEMPLATE_CONTEXT_PROCESSORS|TEMPLATE_DEBUG|USE_I18N|USE_L10N'
)


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
            safe_settings = get_safe_settings()
            log_settings = {}
            for k, v in safe_settings.items():
                if LOGGED_SETTINGS.search(k):
                    log_settings[k] = v
            
            request.debug_logging_stats['settings'] = log_settings
