from unittest.mock import ANY

import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from wishlist.models import Customer, Product, Review, Wishlist

URL = "/api/v1/wishlist/"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestWishlist:
    def test_should_add_item_to_wishlist(self, api_client):
        customer = baker.make(Customer)
        user_token = baker.make(Token, user=User.objects.first())
        product = baker.make(Product)
        api_client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = api_client.post(
            URL,
            data={
                "products": [
                    str(product.id),
                ]
            },
        )
        assert response.status_code == 204
        assert Wishlist.objects.filter(customer=customer, products=product).exists()

    def test_should_not_add_duplicated_item_to_wishlist(self, api_client):
        customer = baker.make(Customer)
        user_token = baker.make(Token, user=User.objects.first())
        product = baker.make(Product)

        api_client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = api_client.post(URL, data={"products": [product.id]})
        assert response.status_code == 204
        assert Wishlist.objects.filter(customer=customer, products=product).exists()
        assert (
            Wishlist.objects.get(customer=customer, products=product)
            .products.all()
            .count()
            == 1
        )

        api_client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = api_client.post(URL, data={"products": [str(product.id)]})
        assert response.status_code == 204
        assert (
            Wishlist.objects.get(customer=customer, products=product)
            .products.all()
            .count()
            == 1
        )

    def test_should_get_wishlist(self, api_client):
        customer = baker.make(Customer)
        user_token = baker.make(Token, user=User.objects.first())
        product = baker.make(Product)
        baker.make(Wishlist, products=[product], customer=customer)
        review = baker.make(Review, product=product, customer=customer)
        api_client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = api_client.get(URL)
        assert response.status_code == 200
        data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "products": [
                        {
                            "id": str(product.id),
                            "review": [
                                {
                                    "id": str(review.id),
                                    "created_at": ANY,
                                    "review": review.review,
                                    "score": review.score,
                                }
                            ],
                            "reviewScore": product.reviewScore(),
                            "title": product.title,
                            "image": ANY,
                            "price": str(product.price),
                            "brand": product.brand,
                        }
                    ]
                },
            ],
        }

        assert data == response.json()

    def test_should_raise_if_product_is_not_uuid(self, api_client):
        baker.make(Customer)
        user_token = baker.make(Token, user=User.objects.first())

        api_client.credentials(HTTP_AUTHORIZATION="Token " + user_token.key)
        response = api_client.post(URL, data={"products": ["1"]})
        assert response.status_code == 400