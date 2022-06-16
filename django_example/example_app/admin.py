from django.contrib import admin

from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Modify the Item admin site views."""

    date_hierarchy = "modified"
    list_display = ("name", "value", "modified")
    ordering = ("-modified",)
    readonly_fields = ("modified",)
    search_fields = ("name",)
