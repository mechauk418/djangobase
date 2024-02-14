from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
# Create your views here.
import datetime
from rest_framework import status, response
from rest_framework.response import Response

class ArticleViewSet(ModelViewSet):

    queryset = Article.objects.all().order_by('-pk')
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(
            create_user = self.request.user
        )

    def retrieve(self, request,pk=None, *args, **kwargs):

        instance = get_object_or_404(self.get_queryset(), pk=pk)
        # 당일날 밤 12시에 쿠키 초기화
        tomorrow = datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=59, second=0)
        expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
        
        # response를 미리 받고 쿠키를 만들어야 한다
        serializer = self.get_serializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        # 쿠키 읽기 & 생성
        if request.COOKIES.get('hit') is not None: # 쿠키에 hit 값이 이미 있을 경우
            cookies = request.COOKIES.get('hit')
            cookies_list = cookies.split('|') # '|'는 다르게 설정 가능 ex) '.'
            if str(pk) not in cookies_list:
                response.set_cookie('hit', cookies+f'|{pk}', expires=expires) # 쿠키 생성
                instance.hits += 1
                instance.save()
    
        else: # 쿠키에 hit 값이 없을 경우(즉 현재 보는 게시글이 첫 게시글임)
            response.set_cookie('hit', pk, expires=expires)
            instance.hits += 1
            instance.save()

        # hits가 추가되면 해당 instance를 serializer에 표시
        serializer = self.get_serializer(instance)

        return response
    


class CommentViewSet(ModelViewSet):

    queryset = Comment.objects.all().order_by('-pk')
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(
            create_user = self.request.user,
            article = Article.objects.get(pk=self.kwargs.get("article_pk"))
        )

    def get_queryset(self):
        
        return super().get_queryset().filter(article=self.kwargs.get("article_pk"))
    

class MyArticleView(ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Article.objects.filter(createuser=user)
        else:
            return Article.objects.none()