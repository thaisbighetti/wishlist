# code
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from wishlist.models import Customer


@receiver(post_save, sender=Customer)
def create_customer(sender, instance, created, **kwargs):
    if created:
        User.objects.create(username=instance.email, email=instance.email)


@receiver(pre_delete, sender=Customer)
def delete_customer(sender, instance, using, **kwargs):
    User.objects.get(username=instance.email).delete()
