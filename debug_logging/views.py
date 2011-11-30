from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext

from debug_logging.models import DebugLogRecord, TestRun

RECORDS_PER_PAGE = 50


def _get_all_test_runs():
    return TestRun.objects.all()


def index(request):
    return render_to_response("debug_logging/index.html", {
        'all_test_runs': _get_all_test_runs(),
    }, context_instance=RequestContext(request))

def delete_runs(request):
    if request.method == "POST":
        runs = map(int, request.POST.getlist("run_id"))
        
        TestRun.objects.filter(pk__in = runs).delete()

    return redirect("debug_logging_index")

def run_detail(request, run_id):
    test_run = get_object_or_404(TestRun, id=run_id)
    
    sort = request.GET.get('sort')
    
    if sort == 'response_time':
        order_by = '-timer_total'
    elif sort == 'sql_queries':
        order_by = '-sql_num_queries'
    elif sort == 'sql_time':
        order_by = '-sql_time'
    else:
        order_by = '-timestamp'
    
    test_run.set_aggregates()
    
    p = Paginator(test_run.records.order_by(order_by), RECORDS_PER_PAGE)
    try:
        page_num = int(request.GET.get('p', 1))
    except ValueError:
        page_num = 1
    page = p.page(page_num)
    
    return render_to_response("debug_logging/run_detail.html", {
        'page': page,
        'test_run': test_run,
        'all_test_runs': _get_all_test_runs(),
    }, context_instance=RequestContext(request))


def record_detail(request, record_id):
    record = get_object_or_404(DebugLogRecord, pk=record_id)
    return render_to_response("debug_logging/record_detail.html", {
        'test_run': record.test_run,
        'record': record,
        'all_test_runs': _get_all_test_runs(),
    }, context_instance=RequestContext(request))
