from rest_framework import serializers

from helper import keys

from blog.models import Blog
from user.serializers import ProfileSerializer


class BlogSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'user', 'title', 'cover_image', 'content', 'created', 'modified']

    def create(self, validated_data):
        data = validated_data
        user = self.context.get(keys.USER)
        return Blog.objects.create(user=user, **data)


class BlogUpdateSerializer(BlogSerializer):
    title = serializers.CharField(required=False, max_length=255)