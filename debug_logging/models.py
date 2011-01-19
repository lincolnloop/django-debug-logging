from django.db import models


class DebugLogRecord(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    
    project_name = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    request_path = models.CharField(max_length=255)
    revision = models.CharField(max_length=40, blank=True, null=True)
    settings = models.TextField(blank=True, null=True)
    
    # Timer stats
    timer_utime = models.DecimalField(max_digits=11, decimal_places=2, blank=True,
                                      null=True)
    timer_stime = models.DecimalField(max_digits=11, decimal_places=2, blank=True,
                                      null=True)
    timer_cputime = models.DecimalField(max_digits=11, decimal_places=2, blank=True,
                                        null=True)
    timer_total = models.DecimalField(max_digits=11, decimal_places=2, blank=True,
                                      null=True)
    timer_vcsw = models.IntegerField(blank=True, null=True)
    timer_ivcsw = models.IntegerField(blank=True, null=True)
    
    # Sql stats
    sql_num_queries = models.IntegerField(blank=True, null=True)
    sql_time = models.DecimalField(max_digits=11, decimal_places=2, blank=True,
                                   null=True)
    sql_queries_pickled = models.TextField(blank=True, null=True)
    
    # Cache stats
    cache_num_calls = models.IntegerField(blank=True, null=True)
    cache_time = models.DecimalField(max_digits=11, decimal_places=2, blank=True,
                                   null=True)
    cache_hits = models.IntegerField(blank=True, null=True)
    cache_misses = models.IntegerField(blank=True, null=True)
    cache_sets = models.IntegerField(blank=True, null=True)
    cache_gets = models.IntegerField(blank=True, null=True)
    cache_get_many = models.IntegerField(blank=True, null=True)
    cache_deletes = models.IntegerField(blank=True, null=True)
    cache_calls = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'DebugLogRecord from %s' % self.timestamp
    
    @property
    def sql_queries(self):
        pass
