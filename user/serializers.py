from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

from helper import keys
from helper.mixins import SerializerMixin

from user.models import User


class RegisterSerializer(SerializerMixin, serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get(keys.EMAIL)
        mobile = data.get(keys.MOBILE)

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this Email already exists.')

        if mobile and User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError('User with this Mobile already exists.')

        return data


class LoginSerializer(SerializerMixin, serializers.Serializer):
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get(keys.EMAIL)
        mobile = data.get(keys.MOBILE)
        password = data.get(keys.PASSWORD)
        try:
            if email:
                user = User.objects.get(email=email)
            elif mobile:
                user = User.objects.get(mobile=mobile)
            else:
                raise serializers.ValidationError('Email/Mobile is required.')
        
            if not user.check_password(password):
                raise serializers.ValidationError('Password is incorrect.')
        except ObjectDoesNotExist:
            raise serializers.ValidationError('User not found.')
        return data


class ChangePasswordSerializer(SerializerMixin, serializers.Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        request = self.context.get(keys.REQUEST)
        password = data.get(keys.PASSWORD)

        user = request.user
        if not user.check_password(password):
            raise serializers.ValidationError('Password is incorrect.')
        return data


class RefreshTokenSerializer(SerializerMixin, serializers.Serializer):
    refresh_token = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'full_name', 'email', 'mobile', 'profile_pic']

    def validate(self, data):
        email = data.get(keys.EMAIL)
        mobile = data.get(keys.MOBILE)

        user = self.instance

        if email and User.objects.exclude(id=user.id).filter(email=email).exists():
            raise serializers.ValidationError('User with this Email already exists.')

        if mobile and User.objects.exclude(id=user.id).filter(mobile=mobile).exists():
            raise serializers.ValidationError('User with this Mobile already exists.')

        return data
