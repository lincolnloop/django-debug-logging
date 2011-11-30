import os.path
import platform
import subprocess

from django.conf import settings
from django.utils.importlib import import_module


def get_project_name():
    return settings.SETTINGS_MODULE.split('.')[0]


def get_hostname():
    return platform.node()


def get_revision():
    vcs = getattr(settings, 'DEBUG_TOOLBAR_CONFIG', {}).get('VCS', None)
    if vcs == 'git':
        module = import_module(settings.SETTINGS_MODULE)
        path = os.path.realpath(os.path.dirname(module.__file__))
        cmd = 'cd %s && git rev-parse --verify --short HEAD' % path
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        proc_stdout, proc_stderr = proc.communicate()
        return proc_stdout


def import_from_string(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured(
            'Error importing module %s: "%s"' % (module, e)
        )
    try:
        instance = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(
            'Module "%s" does not define a "%s" attribute' % (module, attr)
        )
    return instance
