from django.shortcuts import get_object_or_404

import nexus

from debug_logging.models import DebugLogRecord


class DebugLoggingModule(nexus.NexusModule):
    home_url = 'index'
    name = 'debug-logging'
    
    def get_title(self):
        return 'Debug Logging'
    
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        
        urlpatterns = patterns('',
            url(r'^$', self.as_view(self.index), name='index'),
            url(r'^record/(\d+)/$', self.as_view(self.record),
                name='record_detail')
        )
        
        return urlpatterns
    
    def render_on_dashboard(self, request):
        return self.render_to_string('nexus/debug_logging/dashboard.html', {
            'title': 'Debug Logging',
        })
    
    def index(self, request):
        records = DebugLogRecord.objects.order_by('-timestamp')
        
        return self.render_to_response("nexus/debug_logging/index.html", {
            'records': records,
        }, request)
    
    def record(self, request, record_id):
        record = get_object_or_404(DebugLogRecord, pk=record_id)
        return self.render_to_response("nexus/debug_logging/record.html", {
            'record': record,
        }, request)

nexus.site.register(DebugLoggingModule, 'debug-logging')
