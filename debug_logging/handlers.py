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
            
            # Check for a test run meeting the criteria that hasn't ended yet
            test_run = TestRun.objects.filter(end__isnull=True, **filters)
            if test_run:
                record.msg['test_run'] = test_run
            
            instance = DebugLogRecord(**record.msg)
            instance.save()
