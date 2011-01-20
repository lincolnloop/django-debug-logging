from datetime import datetime, timedelta

from django import forms


class DateRangeForm(forms.Form):
    DEFAULT_FROM_DATE = datetime.now() - timedelta(days=7)
    DEFAULT_TO_DATE = datetime.now()
    
    from_date = forms.DateTimeField(initial=DEFAULT_FROM_DATE)
    to_date = forms.DateTimeField(initial=DEFAULT_TO_DATE)
