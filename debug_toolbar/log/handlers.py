import logging

from debug_logging.models import DebugLogRecord


class DBHandler(logging.Handler):
    
    def emit(self, record):
        print '########################## Called'
        if type(record.msg) is dict:
            instance = DebugLogRecord(**record.msg)
            instance.save()
