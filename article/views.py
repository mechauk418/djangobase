from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
# Create your views here.


class ArticleViewSet(ModelViewSet):

    queryset = Article.objects.all().order_by('-pk')
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(
            create_user = self.request.user
        )

    def retrieve(self, request, pk=None, *args, **kwargs):

        instance = get_object_or_404(self.get_queryset(),pk=pk)
        print(instance)

        return super().retrieve(request, *args, **kwargs)
    


class CommentViewSet(ModelViewSet):

    queryset = Comment.objects.all().order_by('-pk')
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(
            create_user = self.request.user,
            article = Article.objects.get(pk=self.kwargs.get("article_pk"))
        )

    def get_queryset(self):
        
        return super().get_queryset().filter(article=self.kwargs.get("article_pk"))
    
    