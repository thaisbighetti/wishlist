from unittest.mock import ANY

import pytest
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from wishlist.models import Customer, Product

URL = "/api/v1/product/"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestProductView:
    def test_should_return_401(self, api_client):
        response = api_client.get(URL)
        assert response.status_code == 401

    def test_should_list_products(self, api_client):
        baker.make(Product, _quantity=2)
        user_token = baker.make(Token)
        api_client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = api_client.get(URL)
        assert response.status_code == 200
        assert len(response.json()["results"]) == 2

    def test_should_retrieve_product(self, api_client):
        product = baker.make(Product)
        user_token = baker.make(Token)
        api_client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = api_client.get(URL + f"{str(product.id)}/")
        assert response.status_code == 200
        assert response.json() == {
            "id": str(product.id),
            "reviewScore": product.reviewScore(),
            "title": product.title,
            "image": ANY,
            "price": str(product.price),
            "brand": product.brand,
        }
