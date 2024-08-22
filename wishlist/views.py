import http
import logging

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wishlist.models import Customer, Product, Wishlist
from wishlist.serializers import (CustomerSerializer, ProductSerializer,
                                  UserTokenSerializer, WishlistSerializer)

logger = logging.getLogger(__name__)


class GetToken(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserTokenSerializer

    def create(self, request):
        user = get_object_or_404(User, username=self.request.data.get("email"))
        token, _ = Token.objects.get_or_create(user=user)
        logger.info("Created token for user with success")
        return Response({"token": token.key}, http.HTTPStatus.OK)


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all().order_by("-created_at")
    http_method_names = ["post", "retrieve", "delete", "head", "put"]

    def get_permissions(self, *args, **kwargs):
        if self.request.method in ["POST"]:
            return []
        else:
            return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        customer = self.get_object()
        try:
            customer.email = request.data["email"]
            customer.save()

            request.user.username = request.data["email"]
            request.user.save()
        except IntegrityError:
            return Response(
                {"error": "Email already exists"}, status=http.HTTPStatus.BAD_REQUEST
            )
        logger.info("Updated user with success")
        return Response(status=http.HTTPStatus.NO_CONTENT)


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    queryset = Wishlist.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticated]
    http_method_names = ["post", "get", "retrieve", "head", "patch"]

    def create(self, request, *args, **kwargs):
        customer = Customer.objects.get(email=request.user)
        wishlist, _ = Wishlist.objects.get_or_create(customer=customer)
        serializer_data = self.serializer_class(data=request.data, instance=wishlist)
        serializer_data.is_valid(raise_exception=True)
        return Response(status=http.HTTPStatus.NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("created_at")
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "retrieve", "head"]
