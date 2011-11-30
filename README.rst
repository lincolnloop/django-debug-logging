====================
Django Debug Logging
====================

Django Debug Logging is a "plugin" for the `Django Debug Toolbar`_ that allows
users to log the debug toolbar statistics to the database during a site crawl.
This allows users to create performance testing plans to exercise the site, and
then review and aggregate the results afterwards to identify performance
problems.

It also provides a basic UI for browsing the details that have been logged to
the database and reviewing aggregated information about test runs.  The UI
borrows a lot from the custom Sphinx theme by the Read the Docs team, and the
Sentry project from Disqus.

The overall goal is to use this tool to monitor performance statistics over
time, so that you can see trends and spikes in the number of queries, cache
misses, cpu time, etc., and identify where in the app the problems are coming
from. It is not intended as a load testing tool, so features like concurrency
and warmup periods will not be part of the initial focus.

Screenshots
-----------

The main Debug Logging frontend view:

.. image:: https://github.com/lincolnloop/django-debug-logging/raw/develop/docs/screenshots/debug_logging.png
   :width: 640px
   :height: 341px
   :scale: 50%
   :alt: Debug Logging main view
   :target: https://github.com/lincolnloop/django-debug-logging/raw/develop/docs/screenshots/debug_logging.png

A test run:

.. image:: https://github.com/lincolnloop/django-debug-logging/raw/develop/docs/screenshots/debug_logging_2.png
   :width: 640px
   :height: 422px
   :scale: 50%
   :alt: Debug Logging aggregated stats
   :target: https://github.com/lincolnloop/django-debug-logging/raw/develop/docs/screenshots/debug_logging_2.png

A log record:

.. image:: https://github.com/lincolnloop/django-debug-logging/raw/develop/docs/screenshots/debug_logging_3.png
   :width: 640px
   :height: 410px
   :scale: 50%
   :alt: Debug Logging detail view
   :target: https://github.com/lincolnloop/django-debug-logging/raw/develop/docs/screenshots/debug_logging_3.png

To Do
-----

We welcome contributions!  Here are some of our main priorities for continued
development:

* Add a --repeat option to the log_urls command so that the urls can be run
  through multiple times.

* Write more complex performance tests that use TestCase classes and log each
  request from the Django test client.

* Graph the aggregated stats of the runs.

* Take more inspiration from Sentry and group hits on the same urls within the
  same run together, showing aggregated and individual stats.

.. _Django Debug Toolbar: https://github.com/django-debug-toolbar/django-debug-toolbar

.. _Picklefield: https://github.com/gintas/django-picklefield
