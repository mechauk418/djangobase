from django.test import TestCase
from .models import *
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from django.urls import reverse
from rest_framework import status


class ArticleAPITestCase(APITestCase):

    def setUp(self):

        register_uri = reverse("accounts:user_registration")

        user_data = {
            "username": "test",
            "email": "test@naver.com",
            "password1": "1q2w3e4r!!",
            "password2": "1q2w3e4r!!"
        }
        response = self.client.post(register_uri,data=user_data)

        client = APIClient()
        client.login(email="test@naver.com", password = '1q2w3e4r!!')
        client.force_authenticate(user=client)
        
    def test_get_article(self):
        article_uri = reverse("article:article_list")

        response = self.client.get(article_uri)

        print(response.content)

        self.assertEqual(response.status_code,200)

    def test_post_article(self):

        article_uri = reverse("article:article_list")
        article_data = {
            "subject":"일반",
            "title":"test_title",
            "content":"test_content"
        }
        response = self.client.post(article_uri,article_data)

        print(response)

        get_response = self.client.get(article_uri)

        print(get_response.content)