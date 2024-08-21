import uuid

from _pydecimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)


class Product(BaseModel):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(null=True, blank=True)
    brand = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def reviewScore(self):
        reviews = Review.objects.filter(product=self)
        if len(reviews) == 0:
            return 0
        return str(
            Decimal(sum([review.score for review in reviews]) / len(reviews)).quantize(
                Decimal("1.00")
            )
        )


class Wishlist(BaseModel):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product, related_name="whishlist_products", blank=True
    )


class Review(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="review_product"
    )
    review = models.TextField()
    score = models.IntegerField(
        default=0, validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
