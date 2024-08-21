import logging

from rest_framework import serializers

from wishlist.models import Customer, Product, Review, Wishlist

logger = logging.getLogger(__name__)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", "score", "id", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    review = serializers.SerializerMethodField()
    reviewScore = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "review", "reviewScore", "title", "image", "price", "brand"]

    def get_review(self, obj):
        reviews = Review.objects.filter(product=obj)
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

    def get_reviewScore(self, data):
        return data.reviewScore()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if (
            self.context.get("request")
            and not "wishlist" in self.context["request"].get_full_path()
        ):
            representation.pop("review")
        return representation


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField("get_products")

    class Meta:
        model = Wishlist
        fields = ("products",)

    def validate(self, attrs):
        for product in dict(self.initial_data).values():
            product_instance = Product.objects.filter(id=product[0]).first()
            if not product_instance:
                logger.info(
                    "Product %s does not exist and will not be added to wishlist",
                    product,
                )
            else:
                self.instance.products.add(product_instance)
        return attrs

    def get_products(self, data):
        products = ProductSerializer(data.products, many=True).data
        return products


class UserTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    token = serializers.UUIDField(required=False)

    class Meta:
        fields = ["token", "email"]
