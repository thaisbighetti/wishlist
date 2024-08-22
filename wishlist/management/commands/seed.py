import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from model_bakery import baker

from wishlist.models import Customer, Product, Review, Wishlist

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        if not User.objects.filter(username="admin").exists():
            User.objects.create_user(
                username="admin",
                password="admin",
                is_staff=True,
                is_active=True,
                is_superuser=True,
            )
            logger.info("Creating user admin password admin")
        if not Customer.objects.all():
            product_1 = baker.make(
                Product,
                title="Celular",
                price=1900,
                brand="Marca de celular legal",
                image=None,
            )
            product_2 = baker.make(
                Product,
                title="Sofá",
                price=1200,
                brand="Marca de sofá legal",
                image=None,
            )
            product_3 = baker.make(
                Product,
                title="Computador",
                price=5000,
                brand="Marca de computador legal",
                image=None,
            )

            baker.make(
                Product,
                title="Video game",
                price=5000,
                brand="Marca de video game legal",
                image=None,
            )
            baker.make(
                Product,
                title="TV",
                price=2000,
                brand="Marca de TV legal",
                image=None,
            )
            baker.make(
                Product,
                title="Geladeira",
                price=3000,
                brand="Marca de Geladeira legal",
                image=None,
            )
            baker.make(
                Product,
                title="Fogão",
                price=2000,
                brand="Marca de Fogão legal",
                image=None,
            )
            baker.make(
                Product,
                title="Maquina de lavar roupa",
                price=2000,
                brand="Marca de maquina de lavar roupa legal",
                image=None,
            )
            baker.make(
                Product,
                title="Ventilador",
                price=2000,
                brand="Marca de ventilador legal",
                image=None,
            )
            baker.make(
                Product,
                title="Ar condicionado",
                price=2000,
                brand="Marca de ar condicionado legal",
                image=None,
            )
            customer = baker.make(
                Customer, email="email123@email.com", name="cara bacana"
            )

            baker.make(
                Review,
                product=product_1,
                review="Celular maneiro",
                score=5,
                customer=customer,
            )
            baker.make(
                Review, product=product_1, review="Celular não tão maneiro", score=2
            )

            baker.make(
                Wishlist, products=[product_1, product_2, product_3], customer=customer
            )
            logger.info("Created initial data with success")
