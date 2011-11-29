import re
from django.views.debug import get_safe_settings
from debug_toolbar.panels.settings_vars import SettingsVarsDebugPanel


class SettingsVarsLoggingPanel(SettingsVarsDebugPanel):
    """Extends the Settings debug panel to enable logging."""

    def __init__(self, *args, **kwargs):
        super(SettingsVarsLoggingPanel, self).__init__(*args, **kwargs)
        self.logged_settings_re = re.compile(
            '|'.join(request.debug_logging['LOGGED_SETTINGS'])
        )

    def process_response(self, request, response):
        if getattr(request, 'debug_logging', {}).get('ENABLED', False):
            # Logging is enabled, so log the settings

            safe_settings = get_safe_settings()
            log_settings = {}
            for k, v in safe_settings.items():
                if self.logged_settings_re.search(k):
                    log_settings[k] = v

            request.debug_logging_stats['settings'] = log_settings
