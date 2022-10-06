from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist

from helper import keys
from helper import response

from user.models import User
from user.serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer, RefreshTokenSerializer, ProfileSerializer


class Register(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description='Register using email/mobile and password.',
        request_body=RegisterSerializer,
        responses={
            '200': openapi.Response(
                description='OK',
                examples={
                    'application/json': {
                        keys.SUCCESS: True,
                        keys.DATA: {
                            keys.ACCESS_TOKEN: 'eyJ0eXAiOiJKV1QiL........',
                            keys.REFRESH_TOKEN: 'eyJ0eXAiOiJKV1QiL........'
                        }
                    }
                },
                schema=None
            )
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data

            email = data.get(keys.EMAIL)
            mobile = data.get(keys.MOBILE)
            password = data.get(keys.PASSWORD)

            user = User.objects.create(email=email, mobile=mobile)
            user.set_password(password)
            user.save(update_fields=[keys.PASSWORD])

            token = RefreshToken.for_user(user)
            update_last_login(None, user)

            data = {
                keys.ACCESS_TOKEN: str(token.access_token),
                keys.REFRESH_TOKEN: str(token),
            }
            return response.response_200(data=data)
        else:
            return response.response_400(error=serializer.errors)


class Login(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description='Login using email/mobile and password.',
        request_body=LoginSerializer,
        responses={
            '200': openapi.Response(
                description='OK',
                examples={
                    'application/json': {
                        keys.SUCCESS: True,
                        keys.DATA: {
                            keys.ACCESS_TOKEN: 'eyJ0eXAiOiJKV1QiL........',
                            keys.REFRESH_TOKEN: 'eyJ0eXAiOiJKV1QiL........'
                        }
                    }
                },
                schema=None
            )
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data

            email = data.get(keys.EMAIL)
            mobile = data.get(keys.MOBILE)

            if email:
                user = User.objects.get(email=email)
            
            if mobile:
                user = User.objects.get(mobile=mobile)

            token = RefreshToken.for_user(user)
            update_last_login(None, user)

            data = {
                keys.ACCESS_TOKEN: str(token.access_token),
                keys.REFRESH_TOKEN: str(token),
            }
            return response.response_200(data=data)
        else:
            return response.response_400(error=serializer.errors)


class ChangePassword(APIView):

    @swagger_auto_schema(
        operation_description='Change password.',
        manual_parameters=[keys.HEADER_TOKEN],
        request_body=ChangePasswordSerializer,
        responses={
            '200': openapi.Response(
                description='OK',
                examples={
                    'application/json': {
                        keys.SUCCESS: True,
                        keys.MESSAGE: 'Password changed.'
                    }
                },
                schema=None
            )
        }
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={keys.REQUEST: request}
        )
        if serializer.is_valid():
            user = request.user
            data = serializer.data

            new_password = data.get(keys.NEW_PASSWORD)

            user.set_password(new_password)
            user.save(update_fields=[keys.PASSWORD])
            return response.response_200(message='Password changed.')
        else:
            return response.response_400(error=serializer.errors)


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description='Refresh token.',
        request_body=RefreshTokenSerializer,
        responses={
            '200': openapi.Response(
                description='OK',
                examples={
                    'application/json': {
                        keys.SUCCESS: True,
                        keys.DATA: {
                            keys.ACCESS_TOKEN: 'eyJ0eXAiOiJKV1QiL........',
                            keys.REFRESH_TOKEN: 'eyJ0eXAiOiJKV1QiL........'
                        }
                    }
                },
                schema=None
            )
        }
    )
    def post(self, request):
        serializer = RefreshTokenSerializer(
            data=request.data,
            context={keys.REQUEST: request}
        )
        if serializer.is_valid():
            data = serializer.data

            refresh_token = data.get(keys.REFRESH_TOKEN)

            try:
                token = RefreshToken(refresh_token)
            except Exception as error:
                return response.response_400(error=str(error))

            access_token = str(token.access_token)

            try:
                token.blacklist()
            except Exception as error:
                return response.response_400(error=str(error))

            token.set_jti()
            token.set_exp()

            data = {
                keys.ACCESS_TOKEN: access_token,
                keys.REFRESH_TOKEN: refresh_token,
            }
            return response.response_200(data=data)
        else:
            return response.response_400(error=serializer.errors)


class Profile(APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_description='Get profile.',
        manual_parameters=[keys.HEADER_TOKEN],
        responses={
            '200': openapi.Response(
                description='OK',
                examples=None,
                schema=ProfileSerializer
            )
        }
    )
    def get(self, request):
        serializer = ProfileSerializer(
            request.user,
            context={keys.REQUEST: request}
        )
        return response.response_200(data=serializer.data)

    @swagger_auto_schema(
        operation_description='Update profile.',
        manual_parameters=[keys.HEADER_TOKEN],
        request_body=ProfileSerializer,
        responses={
            '200': openapi.Response(
                description='OK',
                examples={
                    'application/json': {
                        keys.SUCCESS: True,
                        keys.MESSAGE: 'Profile updated.'
                    }
                },
                schema=None
            )
        }
    )
    def put(self, request):
        serializer = ProfileSerializer(
            instance=request.user,
            data=request.data,
            context={keys.REQUEST: request},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return response.response_200(data=serializer.data, message='Profile updated.')
        else:
            return response.response_400(error=serializer.errors)