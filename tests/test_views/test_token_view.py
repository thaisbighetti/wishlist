from unittest.mock import ANY

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from wishlist.models import Customer, Product

URL = "/api/v1/token/"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestProductsView:
    def test_should_get_token(self, api_client):
        User.objects.create_user(username="email@email.com")
        response = api_client.post(URL, data={"email": "email@email.com"})
        assert response.status_code == 200
        assert response.json() == {"token": ANY}

    def test_should_raise_404_if_user_does_not_exist(self, api_client):
        response = api_client.post(URL, data={"email": "email@email.com"})
        assert response.status_code == 404

    def test_should_raise_404_if_email_not_provided(self, api_client):
        response = api_client.post(URL, data={})
        assert response.status_code == 404

    def test_should_create_token_if_not_exists(self, api_client):
        User.objects.create_user(username="email@email.com")

        response = api_client.post(URL, data={"email": "email@email.com"})
        assert response.status_code == 200

        token = response.json()["token"]
        assert token is not None

        response = api_client.post(URL, data={"email": "email@email.com"})
        assert response.status_code == 200
        assert response.json()["token"] == token
