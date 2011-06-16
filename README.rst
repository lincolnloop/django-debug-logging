====================
Django Debug Logging
====================

Django Debug Logging is a "plugin" for the `Django Debug Toolbar`_ that allows
users to log the debug toolbar statistics to the database during a site crawl.
This allows users to create performance testing plans to exercise the site, and
then review and aggregate the results afterwards to identify performance
problems.

It also provides a basic UI for browsing the details that have been logged to
the database and reviewing aggregated information about test runs.


Prerequisites
-------------

`Django Debug Toolbar`_ - This project is designed to work alongside the Django
Debug Toolbar and extend its functionality to support logging.

Nexus_ - This is a pluggable admin app created by the Disqus team.  It is used
to present the UI for reviewing your debug logs.

Installation
------------

Before you begin, make sure Django Debug Toolbar is configured and working
properly.

Install the project with pip::

    $ pip install django-debug-logging

Next, you'll add *debug_logging* and *nexus* to your INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'debug_logging',
        'nexus',
    )

Now, you'll need to replace the standard DebugToolbarMiddleware with a
middleware that extends it to add logging functionality.

From your MIDDLEWARE_CLASSES setting, remove::

    'debug_toolbar.middleware.DebugToolbarMiddleware',

Replace it with::

    'debug_logging.middleware.DebugLoggingMiddleware',

Now, you'll need to replace a few of the panels with extended versions that
support logging.  If you don't want the data from any one of these panels to
be logged, you can skip it.

From your DEBUG_TOOLBAR_PANELS setting, remove::

    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',

Replace them with::

    'debug_logging.panels.cache.CacheLoggingPanel',
    'debug_logging.panels.settings_vars.SettingsVarsLoggingPanel',
    'debug_logging.panels.sql.SQLLoggingPanel',
    'debug_logging.panels.timer.TimerLoggingPanel',

There are also a couple of panels that are unique to Django Debug Logging that
you may find convenient when logging data over time.  If you'd like, you can
add them to your DEBUG_TOOLBAR_PANELS setting::

    'debug_logging.panels.revision.RevisionLoggingPanel',
    'debug_logging.panels.identity.IdentityLoggingPanel',

Finally, run syncdb to create the models for statistic logging::

    $ python manage.py syncdb

South migrations are included in case migrations are needed when upgrading to
new versions.

**If logging is enabled, any request to your site will result in a new row in
the logging table.** You probably don't want to enable it during regular
day-to-day development.

To enable logging, create a DEBUG_LOGGING_CONFIG setting that looks like this::

    DEBUG_LOGGING_CONFIG = {
        'ENABLED': True,
    }

To prevent any performance impact from the rendering of the Debug
Toolbar, it is not shown.

Settings
--------

There are a few optional DEBUG_LOGGING_CONFIG settings, as well.

* ``SQL_EXTRA``: This setting determines whether the full details of each query
  are logged, or just the number of queries and the total time.  It defaults to
  ``False``.

* ``CACHE_EXTRA``: This determines whether the full details of each cache call
  are logged, or just the summary details. It defaults to `` False``.

Running a Url Test
------------------

A management command is included that uses the test client to hit a list of
urls in sequence, allowing them to be logged to the database.  To use it, first
create a list of urls with a new url on each line.  Lines beginning with # are
ignored.

Then, enable logging and run the *log_urls* management command::

    $ python manage.py log_urls myapp/my_urls.txt

Unless it is run with a verbosity of 0, the command will output status
such as urls that return status codes other than 200, and urls that raise
errors.

Interface
---------

The frontend interface uses the Nexus_ project from the Disqus team.  Once
Nexus is installed, make sure you add *nexus/* to your urls::

    (r'^nexus/', include(nexus.site.urls)),

Nexus should autodetect debug-logging, and the interface should be available
at::

    /nexus/debug-logging/

The Debug Logger will ignore requests made to this frontend interface, so your
log won't be clogged with information you have no use for.

.. _Django Debug Toolbar: https://github.com/django-debug-toolbar/django-debug-toolbar

.. _Nexus: https://github.com/dcramer/nexus

To Do
-----

* Create a model to group log records into 'runs', capturing start date and end
  date and aggregated stats.  This will make it easier to run your url test
  repeatedly over time and see the impact of your changes.

* Graph the aggregated stats of the runs.

* [Maybe] Create a UI that is more user-friendly and not dependent on Nexus.
