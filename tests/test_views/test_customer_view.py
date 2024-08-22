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
    def test_should_return_401_if_not_send_token(self, api_client):
        response = api_client.get(URL)
        assert response.status_code == 401

    def test_should_return_401_if_token_not_exist(self, api_client):
        api_client.credentials(
            HTTP_AUTHORIZATION="Token a1724aa22c40824f430c328b7712eb2d373a0800"
        )
        response = api_client.post(
            URL, data={"name": "name", "email": "email@email.com"}
        )
        assert response.status_code == 401

    def test_should_raise_405_when_get_customer(self, api_client):
        customer = baker.make(Customer)
        user_token = baker.make(Token, user=User.objects.first())
        api_client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = api_client.post(
            URL + f"{customer.id}/", data={"name": "name", "email": "email@email.com"}
        )
        assert response.status_code == 405

    def test_should_change_customer(self, api_client):
        customer = baker.make(Customer, email="email@user.com")
        user = User.objects.first()
        user_token = baker.make(Token, user=user)
        api_client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = api_client.put(
            URL + f"{customer.id}/", data={"name": "name", "email": "email@email.com"}
        )
        user.refresh_from_db()

        assert user.username == "email@email.com"
        assert response.status_code == 204

    def test_should_not_change_customer_with_existing_email(self, api_client):
        customer_1 = baker.make(Customer, email="email@email.com")
        baker.make(Customer, email="user@email.com")

        user_token = baker.make(
            Token, user=User.objects.filter(username=customer_1.email).first()
        )
        api_client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = api_client.put(
            URL + f"{customer_1.id}/", data={"name": "name", "email": "user@email.com"}
        )

        assert response.status_code == 400

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

    def test_patch_customer_without_authentication(self, api_client):
        customer = baker.make(Customer)
        data = {"name": "name"}
        response = api_client.patch(f"{URL}{customer.id}/", data=data)
        assert response.status_code == 401

    def test_delete_customer_without_authentication(self, api_client):
        customer = baker.make(Customer)
        response = api_client.delete(f"{URL}{customer.id}/")
        assert response.status_code == 401
