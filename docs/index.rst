.. django-debug-logging documentation master file, created by
   sphinx-quickstart on Wed Nov 30 09:06:54 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-debug-logging's documentation!
================================================

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

.. _Django Debug Toolbar: https://github.com/django-debug-toolbar/django-debug-toolbar

Contents:

.. toctree::
   :maxdepth: 2
   
   install
   settings
   running

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
