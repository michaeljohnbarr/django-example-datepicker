# Following Django conventions
from .fields import *
from .widgets import *

from django import forms

from example.models import TestModel


class TestModelForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = ('start', 'end')

    def __init__(self, *args, **kwargs):
        super(TestModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field] = DatePickerDateField(localize=True)
