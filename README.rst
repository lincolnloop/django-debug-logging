====================
Django Debug Logging
====================

**NOTE**: This information will quickly become defunct as this project
progresses. The goal is to separate the logging functionality from the
debug_toolbar so that this can function as an independent plugin.

To capture detailed performance statistics during a site crawl, you can enable
the ``debug_logging`` app.  To use it, add ``debug_logging`` to your
INSTALLED_APPS.

Then, create add the following configuration to your *settings.py* file::

    DEBUG_LOGGING_CONFIG = {
        'ENABLED': True,
        'SQL_EXTRA': False,
        'CACHE_EXTRA': False,
    }

* ``ENABLED``: This setting is required.  If enabled, the debug toolbar will
  not be shown.  This is to prevent any performance impact from the rendering
  of the toolbar, such as stats being calculated twice.

* ``SQL_EXTRA``: This optional setting determines whether the full details of
  each query are logged, or just the number of queries and the total time.  It
  defaults to ``False``.

* ``CACHE_EXTRA``: This optional setting determines whether the full details of
  each cache call are logged, or just the summary details.  It defaults to
  `` False``.

Nexus Interface
---------------

A Nexus-based admin interface is included with the ``debug_logging`` app.  If
you have ``nexus`` in your INSTALLED_APPS, it should automatically discover
Debug Logging and present it on the dashboard.
