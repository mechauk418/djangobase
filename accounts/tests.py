from django.test import TestCase
from .models import *
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from django.urls import reverse
from rest_framework import status
# Create your tests here.
import jwt
from django.conf import settings

class UserRegistrationAPITestCase(APITestCase):

    # 회원 가입

    def test_registration(self):

        register_uri = reverse("accounts:user_registration")

        user_data = {
            "username": "test",
            "email": "test@naver.com",
            "password1": "1q2w3e4r!!",
            "password2": "1q2w3e4r!!"
        }

        before = User.objects.all().count()
        response = self.client.post(register_uri,data=user_data)

        after = User.objects.all().count()
        self.assertEqual(response.status_code,201)
        self.assertEqual(before+1,after)


class UserAPITestCase(APITestCase):

    def setUp(self):

        register_uri = reverse("accounts:user_registration")

        user_data = {
            "username": "test",
            "email": "test@naver.com",
            "password1": "1q2w3e4r!!",
            "password2": "1q2w3e4r!!"
        }
        response = self.client.post(register_uri,data=user_data)

    def test_login(self):

        # 로그인 API 테스트
        login_uri = '/accounts/login/'
        login_data = {
            "email": "test@naver.com",
            "password":"1q2w3e4r!!"
        }

        response = self.client.post(login_uri, data=login_data)
        self.assertEqual(response.status_code,200)
        
        # 토큰 검증
        token_verify_uri = '/accounts/token/verify/'
        access_token = response.json()['access']
        verify_response = self.client.post(token_verify_uri, data={'token':access_token} )
        self.assertEqual(verify_response.status_code,200)



    def test_refresh_token(self):

        login_uri = '/accounts/login/'
        login_data = {
            "email": "test@naver.com",
            "password":"1q2w3e4r!!"
        }
        
        # 토큰 refresh 테스트
        response = self.client.post(login_uri, data=login_data)

        token_refresh_uri = '/accounts/token/refresh/'
        refresh_token = response.cookies['refresh_token']
        token_response = self.client.post(token_refresh_uri, headers={'refresh_token' : refresh_token} )
        self.assertEqual(token_response.status_code,200)

        # refresh 검증
        access_token = response.json()['access']
        payload = jwt.decode(
            jwt = access_token,
            key=settings.SECRET_KEY,
            algorithms='HS256'
        )
        jwt_userid = payload['user_id']
        login_user = User.objects.get(email = 'test@naver.com')
        self.assertEqual(jwt_userid, login_user.pk)