from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .models import CustomUser
from .serializers import CustomUserSerializer
from .filters import CustomUserFilter

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filterset_class = CustomUserFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        filtered_queryset = filterset.qs

        return filtered_queryset


class UserMatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            liked_user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"error": "Liked user not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = request.user

        if liked_user == user:
            return Response(
                {"error": "You cannot like yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.liked_users.add(liked_user)

        if user in liked_user.liked_users.all():

            # Sending email to liked user
            send_mail(
                f"You matched with {user.first_name}!",
                f"{user.first_name} liked you! Their email: {user.email}!",
                "noreply@simpconnect.com",
                [liked_user.email],
            )

            # Sending email to current user
            send_mail(
                f"You matched with {liked_user.first_name}!",
                f"{liked_user.first_name} liked you! Their email: {liked_user.email}!",
                "noreply@simpconnect.com",
                [user.email],
            )

            return Response({"match": liked_user.email}, status=status.HTTP_200_OK)

        return Response(
            {"success": "User liked successfully"}, status=status.HTTP_201_CREATED
        )
