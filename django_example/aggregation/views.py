from django.db import models
from django.views.generic.list import ListView

from .filters import MonthlyTotalFilter, PurchaseFilter, AggregatedPurchaseFilter


class Purchases(ListView):
    """View all purchases."""

    template_name = "aggregation/purchases.html"

    def get_queryset(self, **kwargs):
        return AggregatedPurchaseFilter(self.request.GET).qs


class MonthlyTotals(ListView):
    """View all of the monthly totals."""

    template_name = "aggregation/monthly.html"

    def get_queryset(self, **kwargs):
        return MonthlyTotalFilter(self.request.GET).qs
