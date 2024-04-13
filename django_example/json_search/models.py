from django.db import models


class Document(models.Model):
    content = models.JSONField(default=dict)

    class Meta:
        db_table = "document"

    def __str__(self):
        return self.content.get("title", "")


class StringDocument(models.Model):
    title = models.CharField(default="")
    body = models.CharField(default="")

    class Meta:
        db_table = "string_document"

    def __str__(self):
        return self.title
