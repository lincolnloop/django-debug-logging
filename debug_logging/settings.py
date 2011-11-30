import re
from logging import Handler

from django.conf import settings
from django.utils.importlib import import_module

from debug_logging.utils import import_from_string


DEFAULT_LOGGED_SETTINGS = [
    'CACHE_BACKEND', 'CACHE_MIDDLEWARE_KEY_PREFIX', 'CACHE_MIDDLEWARE_SECONDS',
    'DATABASES', 'DEBUG', 'DEBUG_LOGGING_CONFIG', 'DEBUG_TOOLBAR_CONFIG',
    'DEBUG_TOOLBAR_PANELS', 'INSTALLED_APPS', 'INTERNAL_IPS',
    'MIDDLEWARE_CLASSES', 'TEMPLATE_CONTEXT_PROCESSORS', 'TEMPLATE_DEBUG',
    'USE_I18N', 'USE_L10N'
]


DEFAULT_CONFIG = {
    'SQL_EXTRA': False,
    'CACHE_EXTRA': False,
    'BLACKLIST': [],
    'LOGGING_HANDLERS': ('debug_logging.handlers.DBHandler',),
    'LOGGED_SETTINGS': DEFAULT_LOGGED_SETTINGS,
}

# Cache of the logging config.
_logging_config = None


def _get_logging_config():
    """
    Extend the default config with the values provided in settings.py, and then
    conduct some post-processing.
    """
    global _logging_config
    if _logging_config is None:
        _logging_config = dict(DEFAULT_CONFIG,
                               **getattr(settings, 'DEBUG_LOGGING_CONFIG', {}))

        # Instantiate the handlers
        handlers = []
        for handler in _logging_config['LOGGING_HANDLERS']:
            if isinstance(handler, Handler):
                handlers.append(handler())
            elif isinstance(handler, basestring):
                handlers.append(import_from_string(handler)())
        _logging_config['LOGGING_HANDLERS'] = handlers

        # Compile a regex for logged settings
        _logging_config['LOGGED_SETTINGS_RE'] = re.compile(
            '|'.join(_logging_config['LOGGED_SETTINGS'])
        )

    return _logging_config


LOGGING_CONFIG = _get_logging_config()
