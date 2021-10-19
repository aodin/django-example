from django import forms
from django.views.generic.edit import FormView


class AppTextInput(forms.widgets.TextInput):
    template_name = 'widgets/text.html'


class AppExampleForm(forms.Form):
    name = forms.CharField(max_length=64, widget=AppTextInput())


class AppExample(FormView):
    template_name = 'app/example.html'
    form_class = AppExampleForm
