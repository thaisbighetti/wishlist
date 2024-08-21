import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from wishlist.models import Customer

URL = "/api/v1/customer/"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestCustomerView:
    def test_should_return_401(self, api_client):
        response = api_client.get(URL)
        assert response.status_code == 401

    def test_should_return_401_if_token_not_exist(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION="Token a1724aa22c40824f430c328b7712eb2d373a0800")
        response = api_client.post(
            URL, data={"name": "name", "email": "email@email.com"}
        )
        assert response.status_code == 401

    def test_should_change_customer(self, api_client):
        baker.make(Customer)
        user_token = baker.make(Token, user=User.objects.first())
        api_client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = api_client.post(
            URL, data={"name": "name", "email": "email@email.com"}
        )
        assert response.status_code == 201

    def test_should_delete_customer(self, api_client):
        customer = baker.make(Customer)
        user_token = baker.make(Token)
        api_client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = api_client.delete(URL + f"{customer.id}/")
        assert response.status_code == 204
        assert Customer.objects.all().count() == 0

    def test_should_create_customer(self, api_client):
        response = api_client.post(
            URL, data={"name": "name", "email": "email@email.com"}
        )
        assert response.status_code == 201
        assert Customer.objects.all().count() == 1
