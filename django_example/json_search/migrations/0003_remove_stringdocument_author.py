# Generated by Django 4.2 on 2023-04-09 20:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("json_search", "0002_stringdocument"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stringdocument",
            name="author",
        ),
    ]