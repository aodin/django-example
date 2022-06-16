from django.db import models
from django.utils import timezone


class Item(models.Model):
    """An example item with a name, numeric value, and modified timestamp."""

    name = models.CharField(max_length=128)
    value = models.FloatField()
    modified = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """Set the modified timestamp whenever the model is saved."""
        self.modified = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        get_latest_by = "modified"
