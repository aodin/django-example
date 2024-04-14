import csv
from io import StringIO
import string
import time

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from crispy_forms.bootstrap import StrictButton
from django import forms
from django.db import connection, transaction
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
import pandas as pd

from .models import Item


"""
modified = str(timezone.now())
f = StringIO()
writer = csv.writer(f)
created = 0
for row in metrics:
    row += (version.pk, modified)
    writer.writerow(row)
    created += 1

model_table = Item._meta.db_table

columns = [
    "market_id",
    "uom_id",
    "date",
    "company_id",
    "area_id",
    "amount",
    "version_id",
    "modified",
]

f.seek(0)  # Make sure the SQL cursor reads the CSV stream from its start
with connection.cursor() as cursor:
    cursor.copy_from(f, model_table, sep=",", columns=columns)    
"""


class ItemList(ListView):
    """List all items."""

    template_name = "csv_upload/list.html"

    # https://docs.djangoproject.com/en/4.1/ref/class-based-views/generic-display/#listview

    # By default, this view will example a template named `example_app/item_list.html`
    # Use `template_name` to set a different template name
    def get_queryset(self):
        return Item.objects.all().order_by("-modified")[:1000]


class UploadForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.attrs = {"novalidate": ""}
        self.helper.layout = Layout(
            "file",
            Row(
                Column(
                    StrictButton("Upload", type="submit", css_class="btn-primary mt-2"),
                    css_class="col-12 text-end",
                ),
            ),
        )


class UploadView(FormView):
    form_class = UploadForm
    template_name = "csv_upload/upload.html"

    def get_success_url(self):
        return reverse("csv:list")

    def form_valid(self, form):
        f = self.request.FILES["file"]

        # Psycopg2
        # with connection.cursor() as cursor:
        #     cursor.copy_from(
        #         f, Item._meta.db_table, sep=",", columns=["name", "amount", "modified"]
        #     )

        # Psycopg version 3
        with connection.cursor() as cursor:
            with cursor.copy(
                f"COPY table_name (name, amount) FROM STDIN DELIMITER ','"
            ) as copy:
                copy.write(f.read())

        # How to handle AttributeError: 'Cursor' object has no attribute 'copy_from' ?
        # copy r from '/home/y.csv' delimiter ',' csv WITH NULL AS 'null';

        # BadCopyFileFormat at /upload
        # missing data for column "modified"
        # CONTEXT:  COPY csv_upload_item, line 1: "Hello,14.5"

        print("FORM VALID")
        return super().form_valid(form)


class CreateView(View):
    def get(self, request):

        records = [["D", 42.0, None], ["E", -0.1, None]]
        with connection.cursor() as cursor:
            with cursor.copy(
                "COPY table_name (name, amount, modified) FROM STDIN"
            ) as copy:
                for record in records:
                    copy.write_row(record)

        # columns = [f.name for f in Item._meta.get_fields() if not f.primary_key]
        # df = pd.DataFrame(columns=columns)
        # df.loc[0] = ["D", 42.0, None]
        # df.loc[1] = ["E", -0.1, None]

        # print(df)

        # f = StringIO()
        # df.to_csv(f, sep="\t", na_rep=r"\N", index=False, header=False)

        # writer = csv.writer(f, dialect=csv.excel_tab)

        # # UniqueViolation at /create
        # # duplicate key value violates unique constraint "csv_upload_item_pkey"
        # # DETAIL:  Key (id)=(7) already exists.
        # # CONTEXT:  COPY csv_upload_item, line 1

        # writer.writerow(["A", 1, None])
        # writer.writerow(["B", None, timezone.now()])

        # print(f.getvalue())

        # # columns = [f.name for f in Item._meta.get_fields()]
        # columns = [f.name for f in Item._meta.get_fields() if not f.primary_key]
        # print(columns)

        # f.seek(0)  # Make sure the SQL cursor reads the CSV stream from its start
        # with connection.cursor() as cursor:
        #     cursor.copy_from(f, Item._meta.db_table, columns=columns)

        return redirect(reverse("csv:list"))


class SpeedView(View):
    def get(self, request):

        chars = string.ascii_letters

        # Number of objects to create
        n = 100000

        # Methods
        # 1. Django save()
        # 2. save() in transaction
        # 3. Django bulk_create()
        # 4. psycopg2 copy_from()

        start = time.monotonic()

        # (1)
        # for n in range(n):
        # Item(name=chars[n % len(chars)], amount=n).save()
        #   1,000: ELAPSED 0.6927044169860892
        #  10,000: ELAPSED 2.261360957985744
        # 100,000: ELAPSED 22.34775895799976

        # (2)
        # with transaction.atomic():
        #     for n in range(n):
        #         Item(name=chars[n % len(chars)], amount=n).save()

        #   1,000: ELAPSED 0.3011762499809265
        #  10,000: ELAPSED 1.2504991670139134
        # 100,000: ELAPSED 9.415965708962176

        # (3)
        # with transaction.atomic():
        #     items = []
        #     for n in range(n):
        #         items.append(Item(name=chars[n % len(chars)], amount=n))
        #     Item.objects.bulk_create(items)

        #   1,000: ELAPSED 0.09930962498765439
        #  10,000: ELAPSED 0.36136383295524865
        # 100,000: ELAPSED 2.814424417039845

        # (4)
        f = StringIO()
        writer = csv.writer(f, dialect=csv.excel_tab)

        with transaction.atomic():
            for n in range(n):
                writer.writerow([chars[n % len(chars)], n])

            f.seek(0)  # Make sure the SQL cursor reads the CSV stream from its start
            with connection.cursor() as cursor:
                cursor.copy_from(f, Item._meta.db_table, columns=["name", "amount"])

        #   1,000: ELAPSED 0.07664495799690485
        #  10,000: ELAPSED 0.10134770802687854
        # 100,000: ELAPSED 0.3896957919932902

        print("ELAPSED", time.monotonic() - start)

        return redirect(reverse("csv:list"))
