from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('debug_logging.views',
    url(r'^$', 'index', name='index'),
    url(r'^record/(\d+)/$', 'record_detail', name='record_detail')
)
