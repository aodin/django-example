# Generated by Django 4.2 on 2023-04-09 20:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("json_search", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StringDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(default="")),
                ("author", models.CharField(default="")),
                ("body", models.CharField(default="")),
            ],
            options={
                "db_table": "string_document",
            },
        ),
    ]
