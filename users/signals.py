from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User, Balance

@receiver(post_save, sender=User)
def create_balance_for_user(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(owner=instance)