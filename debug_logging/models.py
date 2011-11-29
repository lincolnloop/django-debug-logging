from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import date as date_filter

from picklefield.fields import PickledObjectField


class TestRun(models.Model):
    """Captures overall statistics about a single test run."""
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    project_name = models.CharField(max_length=255, blank=True, null=True)
    hostname = models.CharField(max_length=255, blank=True, null=True)
    revision = models.CharField(max_length=40, blank=True, null=True)

    # Some of these fields aren't used yet, since they are not represented in
    # the UI.  Once they are added to the UI, they'll be added to the
    # set_aggregates method below.
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
        date_format = 'n/j/Y g:i a'
        if self.name:
            return '%s (%s)' % (name, date_filter(self.start, date_format))
        return date_filter(self.start, date_format)

    def get_absolute_url(self):
        return reverse('debug_logging_run_detail', args=[self.id])

    def set_aggregates(self, force=False):
        """
        Sets any aggregates that haven't been generated yet, or recalculates
        them if the force option is indicated.
        """
        aggregates = []

        if not self.avg_time or force:
            aggregates.append(models.Avg('timer_total'))
        if not self.avg_cpu_time or force:
            aggregates.append(models.Avg('timer_cputime'))
        if not self.avg_sql_time or force:
            aggregates.append(models.Avg('sql_time'))
        if not self.avg_sql_queries or force:
            aggregates.append(models.Avg('sql_num_queries'))
        if not self.total_sql_queries or force:
            aggregates.append(models.Sum('sql_num_queries'))
        if not self.max_sql_queries or force:
            aggregates.append(models.Max('sql_num_queries'))

        if aggregates:
            aggregated = self.records.aggregate(*aggregates)

            for key, value in aggregated.items():
                if key == 'timer_total__avg':
                    self.avg_time = value
                elif key == 'timer_cputime__avg':
                    self.avg_cpu_time = value
                elif key == 'sql_time__avg':
                    self.avg_sql_time = value
                elif key == 'sql_num_queries__avg':
                    self.avg_sql_queries = value
                elif key == 'sql_num_queries__sum':
                    self.total_sql_queries = value
                elif key == 'sql_num_queries__max':
                    self.max_sql_queries = value


class DebugLogRecord(models.Model):
    """Captures statistics for individual requests."""
    timestamp = models.DateTimeField(auto_now_add=True)
    test_run = models.ForeignKey(TestRun, related_name='records')

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
