import pytest
from django.contrib.auth.models import User
from django.core.management import call_command

from wishlist.models import Customer, Product, Review, Wishlist


@pytest.mark.django_db
class TestSeed:
    def test_seed(self):
        call_command("seed")
        assert User.objects.filter(username="admin").exists()
        assert Product.objects.count() == 10
        assert Wishlist.objects.count() == 1
        assert Customer.objects.count() == 2
        assert Review.objects.count() == 2
