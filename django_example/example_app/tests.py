from django.test import TestCase

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
        pass
