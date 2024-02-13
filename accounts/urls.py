from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import UserViewSet
from dj_rest_auth.registration.views import RegisterView


app_name="accounts"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("user/", UserViewSet.as_view({"get": "list"}), name="user_list"),
    path("user/<int:pk>", UserViewSet.as_view({"get": "retrieve"}), name="user_detail"),
    path("registration/", RegisterView.as_view() , name="user_registration")
]
