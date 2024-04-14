from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=128)
    amount = models.FloatField(null=True)
    modified = models.DateTimeField(null=True)

    class Meta:
        pass

    def __str__(self) -> str:
        return f"{self.name}, {self.amount}, {self.modified}"
