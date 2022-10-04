from django.urls import path
from user import api


urlpatterns = [
    path('login/', api.Login.as_view()),
    path('profile/', api.Profile.as_view()),
    path('register/', api.Register.as_view()),
    path('change-password/', api.ChangePassword.as_view()),
    path('refresh-token/', api.RefreshTokenView.as_view()),
]
