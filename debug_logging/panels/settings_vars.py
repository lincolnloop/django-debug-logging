from django.views.debug import get_safe_settings
from debug_toolbar.panels.settings_vars import SettingsVarsDebugPanel


class SettingsVarsLoggingPanel(SettingsVarsDebugPanel):
    """Extends the Settings debug panel to enable logging."""

    def process_response(self, request, response):
        super(SettingsVarsLoggingPanel, self).process_response(request, response)
        if getattr(request, 'debug_logging', {}).get('ENABLED', False):
            # Logging is enabled, so log the settings

            safe_settings = get_safe_settings()
            log_settings = {}
            for k, v in safe_settings.items():
                if request.debug_logging['LOGGED_SETTINGS_RE'].search(k):
                    log_settings[k] = v

            request.debug_logging_stats['settings'] = log_settings
