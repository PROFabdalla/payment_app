from djoser.views import UserViewSet, TokenCreateView
from user_app.serializers import (
    CustomUserCreateSerializer,
    CustomTokenCreateSerializers,
)
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model, login
from rest_framework import status
from rest_framework.response import Response
from knox.views import LoginView

User = get_user_model()

# ------------ get data come from (UserSerializer) -------- #
class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == "create":
            return CustomUserCreateSerializer
        return super().get_serializer_class()


class CustomLoginView(LoginView, TokenCreateView):
    serializer_class = CustomTokenCreateSerializers
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            login(request, user)
            response = super().post(request, format=None)
        else:
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(response.data, status=status.HTTP_200_OK)
