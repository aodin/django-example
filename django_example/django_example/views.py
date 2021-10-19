from django import forms
from django.views.generic.edit import FormView


class TextInput(forms.widgets.TextInput):
    pass


class ExampleForm(forms.Form):
    name = forms.CharField(max_length=64, widget=TextInput())


class Example(FormView):
    template_name = 'example.html'
    form_class = ExampleForm
