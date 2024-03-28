from django.urls import path, include
from .views import UserViewSet, kakao_callback, KakaoLogin, google_callback, GoogleLogin
from dj_rest_auth.registration.views import RegisterView

app_name="accounts"

urlpatterns = [
    path("userlist/", UserViewSet.as_view({"get": "list"}), name="user_list"),
    path("user/<int:pk>", UserViewSet.as_view({"get": "retrieve"}), name="user_detail"),
    path("registration/", RegisterView.as_view() , name="user_registration"),
    path(
        "kakao/login/finish/", KakaoLogin.as_view(), name="kakao_login_todjango"
    ),
    path("google/callback/", google_callback, name="google_callback"),
    path(
        "google/login/finish/",
        GoogleLogin.as_view(),
        name="google_login_todjango",
    ),
]
