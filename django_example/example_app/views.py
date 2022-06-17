from django.urls import reverse
from django.views.generic import CreateView, ListView

from .models import Item


class ItemList(ListView):
    """List all items."""

    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/#listview

    # By default, this view will example a template named `example_app/item_list.html`
    # Use `template_name` to set a different template name
    def get_queryset(self):
        return Item.objects.all().order_by("-modified")


class CreateItem(CreateView):
    """Create a new item."""

    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-editing/#createview

    model = Item
    fields = ("name", "value")

    def get_success_url(self):
        return reverse("items:list")
