from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import Article, Comment, LikeArticle, LikeComment
from .serializers import ArticleSerializer, CommentSerializer, LikeCommentSerializer, LikeArticleSerializer
# Create your views here.
import datetime
from rest_framework import status, response, filters
from rest_framework.response import Response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsOwnerOrReadOnly
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination

class PostPageNumberPagination(PageNumberPagination):
    page_size = 20 # 한 페이지 당 항목 개수

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('results', data),
            ('pageCnt', self.page.paginator.num_pages),
            ('curPage', self.page.number),
            ('itemcount',self.page.paginator.count)
        ]))

class ArticleViewSet(ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = Article.objects.all().order_by('-pk')
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('title', 'create_user__username', 'subject', 'content')
    # search_fields = ('title', 'create_user__username', 'content')
    pagination_class=PostPageNumberPagination

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
            response.set_cookie('hit', pk, expires=expires, samesite='Lax')
            instance.hits += 1
            instance.save()

        # hits가 추가되면 해당 instance를 serializer에 표시
        serializer = self.get_serializer(instance)

        return response

    

class CommentViewSet(ModelViewSet):

    queryset = Comment.objects.all().order_by('-pk')
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            create_user = self.request.user,
            article = Article.objects.get(pk=self.kwargs.get("article_pk"))
        )

    def get_queryset(self):
        
        return super().get_queryset().filter(article=self.kwargs.get("article_pk"))
    
from django.http import JsonResponse

class LikeArticleViewSet(ModelViewSet):
    pagination_class=None
    serializer_class = LikeArticleSerializer

    def get_queryset(self):
        article = Article.objects.get(pk=self.kwargs.get('pk'))
        
        return LikeArticle.objects.filter(article = article)

    def create(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs.get("pk"))
        like = LikeArticle.objects.filter(user=self.request.user, article = article)
        comment = {'response':'이미 추천하셨습니다.'}
        if like.exists():
            return JsonResponse(comment)
        return super().create(request, *args, **kwargs)


    def perform_create(self, serializer):
        article = Article.objects.get(pk=self.kwargs.get("pk"))
        like = LikeArticle.objects.filter(user=self.request.user, article = article)
        if like.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer.save(
            user=self.request.user,
            article=Article.objects.get(pk=self.kwargs.get("pk")),
        )

class LikeCommentViewSet(ModelViewSet):

    serializer_class = LikeCommentSerializer

    def get_queryset(self):
        comment = Comment.objects.get(pk=self.kwargs.get('pk'))
        
        return LikeComment.objects.filter(comment = comment)

    def create(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=self.kwargs.get("pk"))
        like = LikeComment.objects.filter(user=self.request.user, comment = comment)
        comments = {'response':'이미 추천하셨습니다.'}
        if like.exists():
            return JsonResponse(comments)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        comment = Comment.objects.get(pk=self.kwargs.get("pk"))
        like = LikeComment.objects.filter(user=self.request.user, comment = comment)
        if like.exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer.save(
            user=self.request.user,
            comment=Comment.objects.get(pk=self.kwargs.get("pk")),
        )

class BestArticleViewSet(ModelViewSet):

    serializer_class = ArticleSerializer
    queryset = Article.objects.annotate(count=Count('article_name')).filter(count__gt=1).order_by('-pk')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('title', 'create_user__username', 'subject', 'content')
    pagination_class = PostPageNumberPagination

class MyArticleViewSet(ModelViewSet):
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('title', 'create_user__username', 'subject', 'content')
    pagination_class=PostPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Article.objects.filter(create_user=user).order_by('-pk')
        
class MyCommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        
        return Comment.objects.filter(create_user=self.request.user)
    

# test