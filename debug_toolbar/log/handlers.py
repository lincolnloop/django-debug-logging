import logging

from debug_toolbar.models import DebugLogRecord


class DBHandler(logging.Handler):
    
    def __init__(self, *args, **kwargs):
        super(DBHandler, self).__init__(*args, **kwargs)
    
    def emit(self, record):
        if type(record.msg) is dict:
            instance = DebugLogRecord(**record.msg)
            instance.save()
