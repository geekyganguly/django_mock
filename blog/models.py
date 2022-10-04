from django.db import models
from tinymce.models import HTMLField

from user.models import User


class Blog(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=255)
    content = HTMLField(blank=True)
    cover_image = models.ImageField(upload_to='blog/cover_image/', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title