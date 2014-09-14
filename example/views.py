# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView

from .models import TestModel
from .forms import TestModelForm


class CreateTestModelView(CreateView):
    model = TestModel
    form_class = TestModelForm
    success_url = reverse_lazy('example_home')
