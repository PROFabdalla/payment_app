from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_app.views import CustomUserViewSet, CustomLoginView
from knox.views import LogoutAllView, LogoutView

app_name = "user_app"


router = DefaultRouter()
router.register("users", CustomUserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", CustomLoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("logoutall/", LogoutAllView.as_view()),
]
