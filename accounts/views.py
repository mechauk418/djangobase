from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialAccount
from allauth.account.adapter import get_adapter
# Create your views here.
from json.decoder import JSONDecodeError
from django.http import JsonResponse
import requests
from rest_framework import status
import os
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view

class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


BASE_URL = "https://api.isdfans.site/"

KAKAO_CALLBACK_URI = "https://www.isdfans.site/login"

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def kakao_callback(request):
    rest_api_key = os.getenv("REST_API_KEY")
    code = request.GET.get('code')
    redirect_uri = KAKAO_CALLBACK_URI
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}"
    )

    token_req_json = token_req.json()
    print(token_req_json)
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    error = profile_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    kakao_account = profile_json.get("kakao_account")
    email = kakao_account.get("email")

    try:
        user = User.objects.get(email = email)
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "kakao":
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 kakao로 가입된 유저
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        # refresh_token을 headers 문자열에서 추출함
        refresh_token = accept.headers['Set-Cookie']
        refresh_token = refresh_token.replace('=',';').replace(',',';').split(';')
        token_index = refresh_token.index(' refresh_token')
        cookie_max_age = 3600 * 24 * 14 # 14 days
        refresh_token = refresh_token[token_index+1]
        accept_json.pop("user", None)
        response_cookie = JsonResponse(accept_json)
        response_cookie.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
        return response_cookie
    
    except User.DoesNotExist:
        
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup", 'error_log':accept_status, "sendcode": data}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴

        accept_json = accept.json()
        # refresh_token을 headers 문자열에서 추출함
        refresh_token = accept.headers['Set-Cookie']
        refresh_token = refresh_token.replace('=',';').replace(',',';').split(';')
        token_index = refresh_token.index(' refresh_token')
        refresh_token = refresh_token[token_index+1]
        cookie_max_age = 3600 * 24 * 14 # 14 days
        accept_json.pop("user", None)
        response_cookie = JsonResponse(accept_json)
        response_cookie.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
        return response_cookie



class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "https://www.isdfans.site/login" 


GOOGLE_CALLBACK_URI = "https://www.isdfans.site/login"  # 프론트 로그인 URI 입력

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def google_callback(request):
    client_id = os.getenv("GOOGLE_CLIENT")
    client_secret = os.getenv("GOOGLE_PASSWORD")
    code = request.GET.get("code")
    """
    Access Token Request
    """
    state = os.getenv("STATE") # 난수
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
    )
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse(
            {"err_msg": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
        )
    email_req_json = email_req.json()
    email = email_req_json.get("email")
    """
    Signup or Signin Request
    """

    cookie_max_age = 3600 * 24 * 14 # 14 days

    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "google":
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 Google로 가입된 유저
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=token_req_json)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        refresh_token = accept.headers['Set-Cookie']
        refresh_token = refresh_token.replace('=',';').replace(',',';').split(';')
        token_index = refresh_token.index(' refresh_token')
        refresh_token = refresh_token[token_index+1]
        accept_json.pop("user", None)
        response_cookie = JsonResponse(accept_json)
        response_cookie.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
        return response_cookie
    
    
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        accept = requests.post("https://api.isdfans.site/accounts/google/login/finish/", data=token_req_json)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        accept_json = accept.json()
        refresh_token = accept.headers['Set-Cookie']
        refresh_token = refresh_token.replace('=',';').replace(',',';').split(';')
        token_index = refresh_token.index(' refresh_token')
        refresh_token = refresh_token[token_index+1]
        print(accept_json)
        accept_json.pop("user", None)
        response_cookie = JsonResponse(accept_json)
        response_cookie.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
        return response_cookie


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client