from django.contrib import admin
from debug_logging.models import TestRun, DebugLogRecord


class TestRunAdmin(admin.ModelAdmin):
    pass
admin.site.register(TestRun, TestRunAdmin)


class DebugLogRecordAdmin(admin.ModelAdmin):
    pass
admin.site.register(DebugLogRecord, DebugLogRecordAdmin)
