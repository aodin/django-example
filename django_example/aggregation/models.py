from django.db import models


class Purchase(models.Model):
    """A purchase."""

    item = models.TextField()
    amount = models.FloatField()
    at = models.DateTimeField(db_index=True)

    def __str__(self):
        return self.item

    class Meta:
        db_table = "purchases"
        get_latest_by = "at"


class AggregatedPurchaseManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().values("item").annotate(total=models.Sum("amount"))
        )


class AggregatedPurchase(Purchase):
    objects = AggregatedPurchaseManager()

    class Meta:
        proxy = True


class MonthlyTotalManager(models.Manager):
    """Aggregate total purchases by month."""

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(month=models.functions.TruncMonth("at"))
            .values("month")
            .annotate(total=models.Sum("amount"))
        )


class MonthlyTotal(Purchase):
    objects = MonthlyTotalManager()

    class Meta:
        proxy = True
