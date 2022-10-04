from django.urls import path

from blog import api


urlpatterns = [
    path('', api.BlogApi.as_view()),
]
