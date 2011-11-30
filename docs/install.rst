Installation
============

Prerequisites
-------------

These requirements are installed automatically by *pip* and *easy_install*, and
are in the included *requirements.pip* file.

`Django Debug Toolbar`_ - This project is designed to work alongside the Django
Debug Toolbar and extend its functionality to support logging.

Picklefield_ - Used to saved pickled versions of settings, sql queries, and
cache calls to the database.

.. _Django Debug Toolbar: https://github.com/django-debug-toolbar/django-debug-toolbar
.. _Picklefield: https://github.com/gintas/django-picklefield

Installing
----------

Before you begin, make sure Django Debug Toolbar is configured and working
properly.

Install the project with pip::

    $ pip install django-debug-logging

This should install django-picklefield as well, which is needed.

Next, you'll add *debug_logging* to your INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'debug_toolbar',
        'debug_logging',
    )

Now, you'll need to replace the standard DebugToolbarMiddleware with a
middleware that extends it to add logging functionality.  The toolbar will
still function normally when logging is disabled.

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

Add the debug logging urls to your urls.py::

    urlpatterns = patterns('',
        ...
        url(r'^debug-logging/', include('debug_logging.urls')),
    )
    
The Debug Logger will ignore requests made to this frontend interface, so your
log won't be clogged with information you have no use for.

Finally, run syncdb to create the models for statistic logging::

    $ python manage.py syncdb

South migrations are included in case migrations are needed when upgrading to
new versions.

Logging
-------

Requests are logged when they contain a 'DJANGO_DEBUG_LOGGING' header set to
True.  This header is added automatically by the 'log_urls' command when it is
used.  To prevent any performance impact from the rendering of the Debug Toolbar,
it is not shown when this header is present.

For the best results, don't use the site while a test run is in progress.
