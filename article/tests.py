from django.test import TestCase
from .models import *
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from django.urls import reverse
from rest_framework import status


class ArticleAPITestCase(APITestCase):

    def setUp(self):

        register_uri = reverse("accounts:user_registration")

        user_data = {
            "username": "tester",
            "email": "test@naver.com",
            "password1": "1q2w3e4r!!",
            "password2": "1q2w3e4r!!"
        }
        self.client.post(register_uri,data=user_data)

        client = APIClient()
        client.login(email="test@naver.com", password = '1q2w3e4r!!')
        client.force_authenticate(user=client)
        
    # 글 목록
    def test_get_article(self):
        article_uri = reverse("article:article_list")

        response = self.client.get(article_uri)

        self.assertEqual(response.status_code,200)

    # 글 작성
    def test_create_article(self):

        article_uri = reverse("article:article_list")
        article_data = {
            "subject":"일반",
            "title":"test_title",
            "content":"test_content"
        }
        response = self.client.post(article_uri,article_data)
        self.assertEqual(response.status_code,201)

    # 글 수정
    def test_update_article(self):

        article_uri = reverse("article:article_list")
        article_data = {
            "subject":"일반",
            "title":"test_title",
            "content":"test_content"
        }
        self.client.post(article_uri,article_data)

        detail_uri = reverse("article:article_detail",args=[1])
        updated_data = {
            "subject":"정보",
            "title":"updated_test_title",
            "content":"test_content"
        }
        response = self.client.put(detail_uri,updated_data)
        
        self.assertEqual(response.status_code,200)

    # 글 삭제
    def test_delete_article(self):
        article_uri = reverse("article:article_list")
        detail_uri = reverse("article:article_detail",args=[1])

        article_data = {
            "subject":"일반",
            "title":"test_title",
            "content":"test_content"
        }
        self.client.post(article_uri,article_data)
        response = self.client.delete(detail_uri)

        self.assertEqual(response.status_code,204)


#댓글 테스트 추후 수정

class CommentAPITestCase(APITestCase):

    def setUp(self):

        register_uri = reverse("accounts:user_registration")
        user_data = {
            "username": "tester",
            "email": "test@naver.com",
            "password1": "1q2w3e4r!!",
            "password2": "1q2w3e4r!!"
        }
        self.client.post(register_uri,data=user_data)
        print(self.client)
        client = APIClient()
        client.login(email="test@naver.com", password = '1q2w3e4r!!')
        client.force_authenticate(user=client)
        print(self.client)
        print(client)
        article_uri = reverse("article:article_list")
        article_data = {
            "subject":"일반",
            "title":"test_title",
            "content":"test_content"
        }
        response = self.client.post(article_uri,article_data)


# 좋아요 테스트 추후 수정
        
# push test