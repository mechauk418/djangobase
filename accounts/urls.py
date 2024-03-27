from django.urls import path, include
from .views import UserViewSet, KakaoLogin
from dj_rest_auth.registration.views import RegisterView

app_name="accounts"

urlpatterns = [
    path("userlist/", UserViewSet.as_view({"get": "list"}), name="user_list"),
    path("user/<int:pk>", UserViewSet.as_view({"get": "retrieve"}), name="user_detail"),
    path("registration/", RegisterView.as_view() , name="user_registration"),
    path(
        "kakao/login/finish/", KakaoLogin.as_view(), name="kakao_login_todjango"
    ),
]
