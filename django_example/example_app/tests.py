from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Item


class ItemTestCase(TestCase):
    """Test the Item model."""

    def test_create(self):
        item = Item.objects.create(
            name="table",
            value=4.5,
        )
        self.assertIsNotNone(item.modified)


class ViewsTestCase(TestCase):
    """Test the views."""

    def test_list(self):
        item = Item.objects.create(name="Item", value=0.0)

        response = self.client.get(reverse("items:list"))
        self.assertContains(response, item.name, status_code=HTTPStatus.OK)
        self.assertEqual(len(response.context["object_list"]), 1)

    def test_empty_list(self):
        response = self.client.get(reverse("items:list"))
        self.assertContains(response, "Items", status_code=HTTPStatus.OK)
        self.assertEqual(len(response.context["object_list"]), 0)

    def test_create(self):
        response = self.client.post(
            reverse("items:create"),
            {"name": "Test", "value": 42},
        )
        self.assertRedirects(
            response,
            reverse("items:list"),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
            fetch_redirect_response=True,
        )
