from django.views.generic.list import ListView

from .filters import MonthlyTotalFilter, PurchaseFilter


class MonthlyTotals(ListView):
    """View all of the monthly totals."""

    template_name = "aggregation/monthly.html"

    def get_queryset(self, **kwargs):
        return PurchaseFilter(self.request.GET).qs
