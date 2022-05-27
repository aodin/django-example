from django.db import models
import django_filters

from .models import Purchase, AggregatedPurchase, MonthlyTotal


class PurchaseFilter(django_filters.FilterSet):
    item = django_filters.CharFilter(lookup_expr="iexact")
    sort = django_filters.OrderingFilter(
        fields=(
            ("item", "item"),
            ("amount", "amount"),
            ("at", "at"),
        ),
    )

    class Meta:
        model = Purchase
        fields = ("amount", "at")


class AggregatedPurchaseFilter(django_filters.FilterSet):
    item = django_filters.CharFilter(lookup_expr="iexact")
    sort = django_filters.OrderingFilter(
        fields=(
            ("item", "item"),
            ("total", "total"),
        ),
    )

    class Meta:
        model = AggregatedPurchase
        fields = ("item",)


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
