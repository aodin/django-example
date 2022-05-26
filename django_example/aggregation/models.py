from django.db import models


class Purchase(models.Model):
    """A purchase."""

    item = models.TextField()
    amount = models.FloatField()
    at = models.DateTimeField(db_index=True)

    def __str__(self):
        return self.item

    class Meta:
        get_latest_by = "at"


class MonthlyTotalManager(models.Manager):
    """Aggregate total purchases by month."""

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                month=models.functions.TruncMonth("at"),
                total=models.Sum("amount"),
            )
        )


class MonthlyTotal(Purchase):
    objects = MonthlyTotalManager()

    class Meta:
        proxy = True
