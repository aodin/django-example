from django.db import models
from django.test import RequestFactory, TestCase
from django.utils import timezone

from .filters import PurchaseFilter, MonthlyTotalFilter
from .models import Purchase


class PurchaseTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create an example model
        Purchase.objects.create(
            item="Breakfast",
            amount=5.90,
            at=timezone.now(),
        )

    def test_model(self):
        results = Purchase.objects.annotate(
            total=models.Sum("amount"),
            # month=models.functions.TruncMonth("at"),
        )
        print(results.query)

    def test_filters(self):
        request = self.factory.get("/")  # NOTE: Only GET query parameters will matter
        filters = PurchaseFilter(request.GET)
        # print(filters.qs.query)

        MonthlyTotalFilter(request.GET)

    def test_queryset(self):
        request = self.factory.get("/?sort=-total")

        queryset = Purchase.objects.values("item").annotate(total=models.Sum("amount"))
        filter = PurchaseFilter(request.GET, queryset=queryset)
        print(filter.qs.query)

    # def test_order_by(self):
    #     Purchase.objects.order_by("total").values("item").annotate(
    #         total=models.Sum("amount")
    #     )
