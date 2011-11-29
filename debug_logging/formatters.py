from logging import Formatter

from django.template import Context, Template


class DjangoTemplatedFormatter(Formatter):

    def __init__(self, fmt=None, datefmt=None):
        """
        Initialize the formatter either with the specified format string, or a
        default as described above. Allow for specialized date formatting with
        the optional datefmt argument (if omitted, you get the ISO8601 format).
        """
        self._fmt = fmt or "{{ message }}"
        self.datefmt = datefmt

    def format(self, record):
        """
        Format the specified record as text.

        The record's attribute dictionary is used as the context and the format
        provided on init is used as the template. Before formatting the
        dictionary, a couple of preparatory steps are carried out. The message
        attribute of the record is computed using LogRecord.getMessage(). If
        the formatting string contains "%(asctime)", formatTime() is called to
        format the event time. If there is exception information, it is
        formatted using formatException() and appended to the message.
        """
        record.message = record.getMessage()
        if "{{ asctime }}" in self._fmt:
            record.asctime = self.formatTime(record, self.datefmt)
        t = Template(self._fmt)
        s = t.render(Context(record.__dict__))
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        return s
