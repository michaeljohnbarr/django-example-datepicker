# ==============================================================================
# IMPORTS
# ==============================================================================
# Django
from django.forms.fields import DateField, DateTimeField

# App
from .widgets import DatePickerWidget

__all__ = ('DatePickerDateField', 'DatePickerDateTimeField')


# ==============================================================================
# FIELDS
# ==============================================================================
class DatePickerDateField(DateField):
    """Extends DateField and adds jQuery DatePicker."""
    widget = DatePickerWidget


class DatePickerDateTimeField(DateTimeField):
    """Extends DateTimeField and adds jQuery DatePicker."""
    widget = DatePickerWidget
