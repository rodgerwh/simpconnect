from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserCreateView, UserMatchView, UserListView

urlpatterns = [
    path("clients/create/", UserCreateView.as_view(), name="user-create"),
    path("clients/<int:id>/match/", UserMatchView.as_view(), name="user-match"),
    path("list/", UserListView.as_view(), name="user-list"),
    path("clients/auth-token/", obtain_auth_token),
]
