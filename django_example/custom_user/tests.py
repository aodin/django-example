from django.test import TestCase

from .models import CustomUser


class CustomUserTestCase(TestCase):
    """Test the CustomUser model."""

    def test_create(self):
        superuser = CustomUser.objects.create_superuser(
            username="superuser",
            email="Superuser@example.com",
            password="secret",
        )
        self.assertTrue(superuser.is_superuser)
