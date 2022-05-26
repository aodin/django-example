from django.contrib import admin

from .models import Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("item", "amount", "at")
    search_fields = ("item",)
    ordering = ("-at",)
