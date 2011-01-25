from copy import deepcopy
from base64 import b64encode, b64decode
from zlib import compress, decompress
try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps

from django.db import models


def dbsafe_encode(value):
    # Encode the pickled value to avoid DjangoUnicodeDecodeError problems.
    # Taken from django-picklefield, by Gintautas Miliauskas
    return b64encode(compress(dumps(deepcopy(value), 2)))


def dbsafe_decode(value):
    return loads(decompress(b64decode(value)))


class DebugLogRecord(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    
    project_name = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    request_path = models.CharField(max_length=255)
    revision = models.CharField(max_length=40, blank=True, null=True)
    settings_pickled = models.TextField(blank=True, null=True)
    
    # Timer stats
    timer_utime = models.FloatField(blank=True, null=True)
    timer_stime = models.FloatField(blank=True, null=True)
    timer_cputime = models.FloatField(blank=True, null=True)
    timer_total = models.FloatField(blank=True, null=True)
    timer_vcsw = models.IntegerField(blank=True, null=True)
    timer_ivcsw = models.IntegerField(blank=True, null=True)
    
    # Sql stats
    sql_num_queries = models.IntegerField(blank=True, null=True)
    sql_time = models.FloatField(blank=True, null=True)
    sql_queries_pickled = models.TextField(blank=True, null=True)
    
    # Cache stats
    cache_num_calls = models.IntegerField(blank=True, null=True)
    cache_time = models.FloatField(blank=True, null=True)
    cache_hits = models.IntegerField(blank=True, null=True)
    cache_misses = models.IntegerField(blank=True, null=True)
    cache_sets = models.IntegerField(blank=True, null=True)
    cache_gets = models.IntegerField(blank=True, null=True)
    cache_get_many = models.IntegerField(blank=True, null=True)
    cache_deletes = models.IntegerField(blank=True, null=True)
    cache_calls_pickled = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'DebugLogRecord from %s' % self.timestamp
    
    def _get_settings(self):
        return dbsafe_decode(self.settings_pickled)

    def _set_settings(self, value):
        self.settings_pickled = dbsafe_encode(value)

    settings = property(_get_settings, _set_settings)
    
    def _get_sql_queries(self):
        return dbsafe_decode(self.sql_queries_pickled)
    
    def _set_sql_queries(self, value):
        self.sql_queries_pickled = dbsafe_encode(value)
    
    sql_queries = property(_get_sql_queries, _set_sql_queries)
    
    def _get_cache_calls(self):
        return dbsafe_decode(self.cache_calls_pickled)
    
    def _set_cache_calls(self, value):
        self.cache_calls_pickled = dbsafe_encode(value)
    
    cache_calls = property(_get_cache_calls, _set_cache_calls)
