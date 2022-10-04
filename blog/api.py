from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from helper import keys
from helper import response
from helper import paginator

from blog.models import Blog
from blog.serializers import BlogListSerializer


class BlogApi(APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_description='Get profile.',
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
                schema=BlogListSerializer
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
                serializer = BlogListSerializer(
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
            serializer = BlogListSerializer(
                instances,
                many=True,
                context={keys.REQUEST: request}
            )
            return response.response_200(data=serializer.data, page_info=page_info)
