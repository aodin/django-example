from django.views.generic import ListView

from .models import Item


class ItemList(ListView):
    """List all items."""

    # By default, this view will example a template named `example_app/item_list.html`
    # Use `template_name` to set a different template
    # https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-display/#listview
    def get_queryset(self):
        return Item.objects.all().order_by("-modified")
