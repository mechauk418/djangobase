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
            "username": "test8",
            "email": "test8@naver.com",
            "password1": "1q2w3e4r!!",
            "password2": "1q2w3e4r!!"
        }

        before = User.objects.all().count()
        response = self.client.post(register_uri,data=user_data)
        access_token = response.json()['access']
        payload = jwt.decode(
            jwt = access_token,
            key=settings.SECRET_KEY,
            algorithms='HS256'
        )
        print(payload['user_id'])
        after = User.objects.all().count()
        self.assertEqual(response.status_code,201)
        self.assertEqual(before+1,after)


class TokenAPITestCase(APITestCase):

    def setUp(self):

        register_uri = reverse("accounts:user_registration")

        user_data = {
            "username": "test8",
            "email": "test8@naver.com",
            "password1": "1q2w3e4r!!",
            "password2": "1q2w3e4r!!"
        }
        response = self.client.post(register_uri,data=user_data)
        access_token = response.json()['access']
        refresh_token = response.json()['refresh']
        print(access_token)
        print(refresh_token)

    # def tokenobtain(self):


