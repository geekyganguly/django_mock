from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from helper import keys
from helper import response
from helper import paginator

from user.models import User
from blog.models import Blog
from blog.serializers import BlogSerializer, BlogUpdateSerializer


class BlogApi(APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_description='Get blog list.',
        manual_parameters=[
            keys.HEADER_TOKEN,
            keys.QUERY_PARAM_PAGE_COUNT,
            keys.QUERY_PARAM_PAGE_NUMBER,
            keys.QUERY_PARAM_SEARCH,
            keys.QUERY_PARAM_FILTER_BY_DATE,
            keys.QUERY_PARAM_USER_ID,
            keys.QUERY_PARAM_BLOG_ID,
        ],
        responses={
            '200': openapi.Response(
                description='OK',
                examples=None,
                schema=BlogSerializer
            )
        }
    )
    def get(self, request):
        blog_id = request.GET.get(keys.BLOG_ID)
        user_id = request.GET.get(keys.USER_ID)
        search = request.GET.get(keys.SEARCH)
        date = request.GET.get(keys.DATE)

        if blog_id:
            try:
                instance = Blog.objects.get(id=blog_id)
                serializer = BlogSerializer(
                    instance,
                    context={keys.REQUEST: request}
                )
                return response.response_200(data=serializer.data)
            except ObjectDoesNotExist:
                return response.response_404()
            except Exception as e:
                return response.response_400(error=str(e))
        else:   
            instances = Blog.objects.all().order_by('created')

            if user_id:
                instances = instances.filter(user__id=user_id)

            if date:
                instances = instances.filter(created=date)
            
            if search:
                instances = instances.filter(Q(title__icontains=search) | Q(content__icontains=search))
            
            instances, page_info = paginator.apply_pagination(request, instances)
            serializer = BlogSerializer(
                instances,
                many=True,
                context={keys.REQUEST: request}
            )
            return response.response_200(data=serializer.data, page_info=page_info)


    @swagger_auto_schema(
        operation_description='Add blog.',
        manual_parameters=[
            keys.HEADER_TOKEN,
            keys.QUERY_PARAM_USER_ID,
        ],
        request_body=BlogSerializer,
        responses={
            '200': openapi.Response(
                description='OK',
                examples={
                    'application/json': {
                        keys.SUCCESS: True,
                        keys.MESSAGE: 'Post created.'
                    }
                },
                schema=None
            )
        }
    )
    def post(self, request):
        user_id = request.GET.get(keys.USER_ID)
        
        if not user_id:
            return response.response_400(error=f'{keys.USER_ID} is required.')

        try:
            user = User.objects.get(id=user_id)
            serializer = BlogSerializer(
                data=request.data, 
                context={
                    keys.REQUEST: request,
                    keys.USER: user
                }
            )
            if serializer.is_valid():
                serializer.save()
                return response.response_200(data=serializer.data, message='Post created.')
            else:
                return response.response_400(error=serializer.errors)
        except ObjectDoesNotExist:
            return response.response_404()
        except Exception as e:
            return response.response_400(error=str(e))


    @swagger_auto_schema(
        operation_description='Update blog.',
        manual_parameters=[
            keys.HEADER_TOKEN,
            keys.QUERY_PARAM_BLOG_ID
        ],
        request_body=BlogUpdateSerializer,
        responses={
            '200': openapi.Response(
                description='OK',
                examples={
                    'application/json': {
                        keys.SUCCESS: True,
                        keys.MESSAGE: 'Blog updated.'
                    }
                },
                schema=None
            )
        }
    )
    def put(self, request):
        blog_id = request.GET.get(keys.BLOG_ID)

        if not blog_id:
            return response.response_400(error=f'{keys.BLOG_ID} is required.')

        try:
            instance = Blog.objects.get(id=blog_id)
            serializer = BlogUpdateSerializer(
                instance=instance,
                data=request.data,
                context={keys.REQUEST: request},
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return response.response_200(data=serializer.data, message='Blog updated.')
            else:
                return response.response_400(error=serializer.errors)
        except ObjectDoesNotExist:
            return response.response_404()
        except Exception as e:
            return response.response_400(error=str(e))


    @swagger_auto_schema(
        operation_description='Delete a blog.',
        manual_parameters=[
            keys.HEADER_TOKEN,
            keys.QUERY_PARAM_BLOG_ID,
        ],
        responses={
            '200': openapi.Response(
                description='OK',
                examples={
                    'application/json': {
                        keys.SUCCESS: True,
                        keys.MESSAGE: 'Post deleted.'
                    }
                },
                schema=None
            )
        }
    )
    def delete(self, request):
        blog_id = request.GET.get(keys.BLOG_ID)

        if not blog_id:
            return response.response_400(error=f'{keys.BLOG_ID} is required.')

        try:
            instance = Blog.objects.get(id=blog_id)
            instance.delete()
            return response.response_200(message='Post deleted.')
        except ObjectDoesNotExist:
            return response.response_404()
        except Exception as e:
            return response.response_400(error=str(e))

