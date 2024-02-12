from django.test import TestCase
from .models import *
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from django.urls import reverse
from rest_framework import status

# class userAPITestCase(APITestCase):

#     # 회원 가입

#     def test_registration(self):

#         register_uri = reverse("accounts:register")