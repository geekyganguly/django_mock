from rest_framework import serializers

from blog.models import Blog
from user.serializers import ProfileSerializer


class BlogListSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = Blog
        fields = ['id', 'user', 'title', 'cover_image', 'content', 'created', 'modified']
