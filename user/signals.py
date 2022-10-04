from django.db.models.signals import pre_save
from django.dispatch import receiver

from helper.utils import Generator

from user.models import User


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    if not instance.id:
        # generate and set username
        if not instance.username:
            instance.username = Generator.generate_username()
            while User.objects.filter(username=instance.username).exists():
                instance.username = Generator.generate_username()
