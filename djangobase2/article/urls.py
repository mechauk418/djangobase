from django.urls import path
from .views import (
    ArticleViewSet, CommentViewSet, MyArticleViewSet, 
    LikeArticleViewSet, LikeCommentViewSet, BestArticleViewSet,
    MyCommentViewSet,envview,metadate
    )

app_name="article"


urlpatterns = [
    path("", ArticleViewSet.as_view({"get": "list", "post":'create',}), name="article_list"),
    path("<int:pk>/", ArticleViewSet.as_view({"get": "retrieve", "put":"update", "delete":"destroy", "patch":"partial_update"}), name="article_detail"),
    path("<int:article_pk>/comment/", CommentViewSet.as_view({"get": "list", "post":'create',}), name="comment_list"),
    path("<int:article_pk>/comment/<int:pk>", CommentViewSet.as_view({"get": "retrieve", "put":"update", "delete":"destroy", "patch":"partial_update"}), name="comment_detail"),
    path("<int:pk>/like/", LikeArticleViewSet.as_view({"get": "list", "post":"create"}), name="like_article"),
    path("<int:article_pk>/comment/<int:pk>/like/", LikeCommentViewSet.as_view({"get": "list", "post":"create"}), name="like_comment"),
    path("bestarticle/", BestArticleViewSet.as_view({"post": "create", "get": "list"}), name="bestarticle"),
    path("myarticle/", MyArticleViewSet.as_view({"get": "list"}), name="myarticle"),
    path("mycomment/", MyCommentViewSet.as_view({"get": "list"}), name="mycomment"),
    path("getenv",envview),
    path("metadate",metadate)
]
