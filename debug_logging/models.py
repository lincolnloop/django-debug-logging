from django.db import models
from picklefield.fields import PickledObjectField


class TestRun(models.Model):
    """Captures overall statistics about a single test run."""
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    project_name = models.CharField(max_length=255, blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    revision = models.CharField(max_length=40, blank=True, null=True)
    
    avg_time = models.FloatField(blank=True, null=True)
    total_time = models.FloatField(blank=True, null=True)
    avg_cpu_time = models.FloatField(blank=True, null=True)
    total_cpu_time = models.FloatField(blank=True, null=True)
    
    avg_sql_time = models.FloatField(blank=True, null=True)
    total_sql_time = models.FloatField(blank=True, null=True)
    avg_sql_queries = models.FloatField(blank=True, null=True)
    total_sql_queries = models.IntegerField(blank=True, null=True)
    max_sql_queries = models.IntegerField(blank=True, null=True)
    
    avg_cache_hits = models.FloatField(blank=True, null=True)
    total_cache_hits = models.IntegerField(blank=True, null=True)
    avg_cache_misses = models.FloatField(blank=True, null=True)
    total_cache_misses = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return u'TestRun started on %s' % self.start


class DebugLogRecord(models.Model):
    """Captures statistics for individual requests."""
    timestamp = models.DateTimeField(auto_now_add=True)
    test_run = models.ForeignKey(TestRun)
    
    request_path = models.CharField(max_length=255)
    settings = PickledObjectField(compress=True, blank=True, null=True)
    
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
    sql_queries = PickledObjectField(compress=True, blank=True, null=True)
    
    # Cache stats
    cache_num_calls = models.IntegerField(blank=True, null=True)
    cache_time = models.FloatField(blank=True, null=True)
    cache_hits = models.IntegerField(blank=True, null=True)
    cache_misses = models.IntegerField(blank=True, null=True)
    cache_sets = models.IntegerField(blank=True, null=True)
    cache_gets = models.IntegerField(blank=True, null=True)
    cache_get_many = models.IntegerField(blank=True, null=True)
    cache_deletes = models.IntegerField(blank=True, null=True)
    cache_calls = PickledObjectField(compress=True, blank=True, null=True)

    def __unicode__(self):
        return u'DebugLogRecord from %s' % self.timestamp
