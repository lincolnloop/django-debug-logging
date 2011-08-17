import logging

from debug_logging.models import TestRun, DebugLogRecord


class DBHandler(logging.Handler):
    
    def emit(self, record):
        if type(record.msg) is dict:
            # Pull the project name, hostname, and revision out of the record
            filters = {}
            for key in ('project_name', 'hostname', 'revision'):
                if record.msg.has_key(key):
                    filters[key] = record.msg.pop(key)
            
            # Find the open test run for this project
            try:
                test_run = TestRun.objects.get(end__isnull=True, **filters)
            except TestRun.DoesNotExist:
                # Don't log this request if there isn't an open TestRun
                return
            record.msg['test_run'] = test_run
            
            instance = DebugLogRecord(**record.msg)
            instance.save()
