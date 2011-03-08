import os

import django.views.static
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Avg, Max
from django.shortcuts import get_object_or_404

import nexus

from debug_logging.forms import DateRangeForm
from debug_logging.models import DebugLogRecord

RECORDS_PER_PAGE = 50


class DebugLoggingModule(nexus.NexusModule):
    home_url = 'index'
    name = 'debug-logging'
    
    def get_title(self):
        return 'Debug Logging'
    
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        
        urlpatterns = patterns('',
            url(r'^m/(.*)$', self.as_view(self.media),
                name='media'),
            url(r'^$', self.as_view(self.index), name='index'),
            url(r'^record/(\d+)/$', self.as_view(self.record),
                name='record_detail')
        )
        
        return urlpatterns
    
    def render_on_dashboard(self, request):
        return self.render_to_string('nexus/debug_logging/dashboard.html', {
            'title': 'Debug Logging',
        })
    
    def media(self, request, path):
        root = getattr(settings, 'DEBUG_LOGGING_CONFIG', {}
            ).get('MEDIA_ROOT', None)
        if root is None:
            parent = os.path.abspath(os.path.dirname(__file__))
            root = os.path.join(parent, 'media', 'debug_logging')
        return django.views.static.serve(request, path, root)

    
    def index(self, request):
        from_date = DateRangeForm.DEFAULT_FROM_DATE
        to_date = DateRangeForm.DEFAULT_TO_DATE
        sort = None
        if request.GET:
            form = DateRangeForm(data=request.GET)
            if form.is_valid():
                if form.cleaned_data.get('from_date'):
                    from_date = form.cleaned_data['from_date']
                if form.cleaned_data.get('to_date'):
                    to_date = form.cleaned_data['to_date']
            
            sort = request.GET.get('sort')
        else:
            form = DateRangeForm()
        
        if sort == 'response_time':
            order_by = '-timer_total'
        elif sort == 'sql_queries':
            order_by = '-sql_num_queries'
        elif sort == 'sql_time':
            order_by = '-sql_time'
        else:
            order_by = '-timestamp'
        
        records = DebugLogRecord.objects.filter(
            timestamp__gte=from_date,
            timestamp__lte=to_date,
        ).order_by(order_by)
        
        aggregates = records.aggregate(
            Avg('timer_total'),
            Avg('timer_cputime'),
            Avg('sql_time'),
            Avg('sql_num_queries'),
            Max('sql_num_queries'),
        )
        
        p = Paginator(records, RECORDS_PER_PAGE)
        try:
            page_num = int(request.GET.get('p', 1))
        except ValueError:
            page_num = 1
        page = p.page(page_num)
        
        return self.render_to_response("nexus/debug_logging/index.html", {
            'form': form,
            'page': page,
            'from_date': from_date,
            'to_date': to_date,
            'aggregates': aggregates,
        }, request)
    
    def record(self, request, record_id):
        record = get_object_or_404(DebugLogRecord, pk=record_id)
        return self.render_to_response("nexus/debug_logging/record.html", {
            'record': record,
        }, request)

nexus.site.register(DebugLoggingModule, 'debug-logging')
