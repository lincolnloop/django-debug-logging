from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('debug_logging.views',
    url(r'^$', 'index', name='debug_logging_index'),
    url(r'^run/(\d+)/$', 'run_detail', name='debug_logging_run_detail'),
    url(r'^record/(\d+)/$', 'record_detail', name='debug_logging_record_detail'),
)
