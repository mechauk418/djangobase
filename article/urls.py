from django.urls import path
from .views import ArticleViewSet, CommentViewSet

urlpatterns = [
    path("article/", ArticleViewSet.as_view({"get": "list", "post":'create',}), name="article_list"),
    path("comment/", CommentViewSet.as_view({"get": "list", "post":'create',}), name="comment_list"),
]
