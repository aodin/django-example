from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from crispy_forms.bootstrap import StrictButton
from django import forms
from django.urls import reverse
from django.views.generic import CreateView, ListView


from .models import Item


class ItemList(ListView):
    """List all items."""

    # https://docs.djangoproject.com/en/4.1/ref/class-based-views/generic-display/#listview

    # By default, this view will example a template named `example_app/item_list.html`
    # Use `template_name` to set a different template name
    def get_queryset(self):
        return Item.objects.all().order_by("-modified")


class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ("name", "value")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs = {"novalidate": ""}
        self.helper.layout = Layout(
            "name",
            "value",
            Row(
                Column(
                    StrictButton("Create", type="submit", css_class="btn-primary mt-2"),
                    css_class="col-12 text-end",
                ),
            ),
        )


class CreateItem(CreateView):
    """Create a new item."""

    form_class = CreateItemForm
    template_name = "example_app/item_form.html"

    # https://docs.djangoproject.com/en/4.1/ref/class-based-views/generic-editing/#createview

    def get_success_url(self):
        return reverse("items:list")
