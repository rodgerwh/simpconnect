from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserCreateView

urlpatterns = [
    path("clients/create/", UserCreateView.as_view(), name="user-create"),
    path("clients/auth-token/", obtain_auth_token),
]
