from django.urls import path
from .views import ArticleViewSet, CommentViewSet

urlpatterns = [
    path("", ArticleViewSet.as_view({"get": "list", "post":'create',}), name="article_list"),
    path("<int:pk>/", ArticleViewSet.as_view({"get": "retrieve", "put":"update", "delete":"destroy", "patch":"partial_update"}), name="article_detail"),
    path("<int:article_pk>/comment/", CommentViewSet.as_view({"get": "list", "post":'create',}), name="comment_list"),
    path("<int:article_pk>/comment/<int:pk>", CommentViewSet.as_view({"get": "retrieve", "put":"update", "delete":"destroy", "patch":"partial_update"}), name="comment_detail"),
]
