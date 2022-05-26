from django.views.generic.list import ListView

from .filters import MonthlyTotalFilter, PurchaseFilter


class Purchases(ListView):
    """View all purchases."""

    template_name = "aggregation/purchases.html"

    def get_queryset(self, **kwargs):
        return PurchaseFilter(self.request.GET).qs


class MonthlyTotals(ListView):
    """View all of the monthly totals."""

    template_name = "aggregation/monthly.html"

    def get_queryset(self, **kwargs):
        return MonthlyTotalFilter(self.request.GET).qs
