from django.db import models
from django.contrib.auth.models import AbstractUser

from helper.mixins import ModelUpdateMixin


class User(AbstractUser, ModelUpdateMixin):
    email = models.EmailField(unique=True, blank=True)
    mobile = models.CharField(max_length=10, unique=True, blank=True)
    profile_pic = models.ImageField(upload_to='user/profile_pic/', blank=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

