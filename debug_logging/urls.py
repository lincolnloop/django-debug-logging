from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('debug_logging.views',
    url(r'^$', 'index', name='index'),
    url(r'^run/(\d+)/$', 'run_detail', name='run_detail'),
    url(r'^record/(\d+)/$', 'record_detail', name='record_detail'),
    
    # Ajax urls
    url(r'^start-run/$', 'start_run', name='start_run'),
)
