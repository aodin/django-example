import django_filters

from .models import Purchase, MonthlyTotal


class PurchaseFilter(django_filters.FilterSet):
    item = django_filters.CharFilter(lookup_expr="iexact")
    sort = django_filters.OrderingFilter(
        fields=(
            ("at", "at"),
            ("amount", "amount"),
        ),
    )

    class Meta:
        model = Purchase
        fields = ("amount", "at")


class MonthlyTotalFilter(django_filters.FilterSet):
    sort = django_filters.OrderingFilter(
        fields=(
            ("month", "month"),
            ("total", "total"),
        ),
    )

    class Meta:
        model = MonthlyTotal
        fields = ("item",)
