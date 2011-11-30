Settings
========

* ``SQL_EXTRA``: This setting determines whether the full details of each query
  are logged, or just the number of queries and the total time.  It defaults to
  ``False``.

* ``CACHE_EXTRA``: This determines whether the full details of each cache call
  are logged, or just the summary details. It defaults to `` False``.

* ``BLACKLIST``: Add a list of url prefixes that you would like to exclude from
  logging here.  The url for the Debug Logging frontend interface is added to
  this blacklist automatically.
